"""
    Token authentication 
    =====================
    
    Simple token based authentication - safe and sound.
        
"""

from flask import Blueprint, current_app as app, request, Response, abort, jsonify
from eve.methods.post import post_internal
from eve.methods.patch import patch_internal
from eve.methods.get import getitem_internal
from ext.app.eve_helper import eve_abort, eve_response, is_mongo_alive
import datetime
import arrow
from time import sleep
from uuid import uuid4
from base64 import b64encode
import traceback
from ext.app.decorators import require_token

import requests
from ext.scf import LUNGO_HEADERS, LUNGO_URL

# Token auth - oauth
import jwt

ISSUER = 'nlf-auth-server'
JWT_LIFE_SPAN = 1800
REALM = 'mi.nif.no'

Authenticate = Blueprint('Authenticate', __name__, )
import os.path


def _get_public_key():
    public_key = None
    with open('fnlfbeta-public.pem', 'rb') as f:
        public_key = f.read()
    return public_key


def create_user(username):
    # melwin_user, _, _, status = getitem_internal(resource='legacy_melwin_users', **{'id': username})

    resp = requests.get('{}/persons/{}'.format(LUNGO_URL, username),
                        headers=LUNGO_HEADERS)

    if resp.status_code == 200:

        try:
            user_response, _, _, user_code, header = post_internal(resource=app.globals['auth']['users_collection'],
                                                                   payl={'id': username},
                                                                   skip_validation=True)
        except:
            app.logger.exception("503: Could not create (POST) new user %i" % username)
            return False

        try:
            auth_response, _, _, auth_code, header = post_internal(resource='users_auth',
                                                                   payl={'id': username,
                                                                         'user': user_response['_id'],
                                                                         'auth': {"token": "",
                                                                                  "valid": ""}},
                                                                   skip_validation=True)
        except:
            app.logger.exception("%i: Could not create (mongo insert) user %i auth item" % (auth_code, username))
            return False

        # Verify both post's response codes
        if user_code == 201 and auth_code == 201:
            return True
        else:
            try:
                from eve.methods.delete import deleteitem_internal
                if '_id' in user_response:
                    _, _, _, code = deleteitem_internal(resource=app.globals['auth']['users_collection'],
                                                        concurrency_check=False,
                                                        suppress_callbacks=True,
                                                        **{'_id': user_response['_id']})
                    app.logger.info("Deleted user from users")
                if '_id' in auth_response:
                    _, _, _, code = deleteitem_internal(resource='users_auth',
                                                        concurrency_check=False,
                                                        suppress_callbacks=True,
                                                        **{'_id': auth_response['_id']})
                    app.logger.info("Deleted user from users_auth")
            except:
                app.logger.exception("Delete operation of user %i from users and users_auth but failed" % username)

    return False

def _get_acl_roles(person_id):
    resp = requests.get('{}/acl/{}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS)
    if resp.status_code == 200:
        return resp.json()['_items']

    return []

@Authenticate.route("/authenticate", methods=['POST'])
def login():
    username = None
    password = None
    logged_in = False

    # Request via json
    rq = request.get_json()

    try:
        username = rq['username']
        password = rq['password']
    except:
        # Now it will fail in the next if
        pass

    if username == 'access_token':

        try:
            public_key = _get_public_key()
            decoded_token = jwt.decode(password, public_key, issuer=ISSUER, algorithm='HS256')
            logged_in = True
            # melwin_id or person_id
            person_id = decoded_token.get('person_id', None)
            melwin_id = decoded_token.get('melwin_id', None)
            if person_id is None:
                eve_abort(401, 'Could not validate the token, could not find username')
            else:
                #  print('Username', person_id)
                person_id = int(person_id)

        except jwt.exceptions.InvalidTokenError:
            logged_in = False
            eve_abort(401, 'Could not validate the token, InvalidTokenError')
        except jwt.exceptions.InvalidSignatureError:
            logged_in = False
            eve_abort(401, 'Could not validate the token, InvalidSignatureError')
        except jwt.exceptions.InvalidIssuerError:
            logged_in = False
            eve_abort(401, 'Could not validate the token, InvalidIssuerError')
        except jwt.exceptions.ExpiredSignatureError:
            logged_in = False
            eve_abort(401, 'Could not validate the token, ExpiredSignatureError')
        except Exception as e:
            logged_in = False
            eve_abort(401, 'Could not validate your token {}'.format(e))
    else:
        eve_abort(401, 'Could not make sense of your request')

    # Now process user and successful authentication
    if logged_in is True:

        try:
            user, last_modified, etag, status = getitem_internal(resource='users', **{'id': person_id})
        except:
            user = None
            if not is_mongo_alive():
                eve_abort(502, 'Network problems')

        # If not existing, make from melwin!
        if user is None or status != 200:
            if not create_user(person_id):
                app.logger.error("502: Could not create user %i from Melwin" % person_id)
                eve_abort(502, 'Could not create user from Melwin')
            else:
                app.logger.info("Created user %i" % person_id)

        # Got that user, fix acl's!
        response, last_modified, etag, status = patch_internal(resource='users',
                                                               payload={'acl_roles': _get_acl_roles(person_id),
                                                                        'melwin_id': melwin_id},
                                                               concurrency_check=False,
                                                               **{'id': person_id})


        # token = uuid5(uuid4(),rq['username'])
        token = uuid4().hex

        # valid = utc.replace(hours=+2)  # @bug: utc and cet!!!
        utc = arrow.utcnow()
        valid = utc.replace(seconds=+app.config['AUTH_SESSION_LENGHT'])
        # Pure datetime
        # valid = datetime.datetime.now() + datetime.timedelta(seconds=60)

        try:
            response, last_modified, etag, status = patch_internal('users_auth',
                                                                   payload={'auth': {'token': token,
                                                                                     'valid': valid.datetime}},
                                                                   concurrency_check=False, **{'id': person_id})
            if status != 200:
                app.logger.error("Could not insert token for %i" % person_id)

        except:
            app.logger.exception("Could not update user %i auth token" % person_id)
            eve_abort(500, "Could not update user %i auth token" % person_id)

        t = '%s:' % token
        b64 = b64encode(t.encode('utf-8'))

        """return jsonify(**{'success': True,
                  'token': token,
                  'token64': b64,
                  'valid': valid,
                  })"""

        return eve_response(data={'success': True,
                                  'username': person_id,
                                  'token': token,
                                  'token64': b64.decode('utf-8'),
                                  'valid': valid.datetime},
                            status=200)

    # On error sleep a little against brute force
    sleep(1)

    return eve_response({'success': False, 'username': None, 'token': None, 'token64': None, 'valid': None,
                         'message': 'Wrong username or password'})


@Authenticate.route("/whoami", methods=['GET'])
@Authenticate.route("/self", methods=['GET'])
@require_token()
def get_user():
    """A simple whoami
    Only return 'I am username'"""

    try:
        response, last_modified, etag, status = getitem_internal(resource='users', **{'id': app.globals['id']})

        if status == 200 and '_id' in response:
            return eve_response(data={'iam': response['id']})
    except:
        app.logger.error("Unknown error in get_user")
        return eve_abort(500, 'Unknown error occurred')


"""
@Authenticate.route("/groups", methods=['GET'])
@require_token()
def get_user_groups():
    return eve_response(data=app.globals['acl'])

"""
