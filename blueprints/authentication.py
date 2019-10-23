"""
    Token authentication 
    =====================
    
    Simple token based authentication - safe and sound.
        
"""

from flask import Blueprint, current_app as app, request, Response, abort, jsonify
from eve.methods.post import post_internal
from eve.methods.patch import patch_internal
from eve.methods.get import getitem_internal, get_internal
from ext.app.eve_helper import eve_abort, eve_response, is_mongo_alive
from datetime import datetime, timedelta
import arrow
from time import sleep
from uuid import uuid4
from base64 import b64encode
import traceback
from ext.app.decorators import require_token
from ext.auth.user import User
import ext.app.lungo as lungo
# Token auth - oauth
import jwt

ISSUER = 'nlf-auth-server'
JWT_LIFE_SPAN = 1800
REALM = 'mi.nif.no'

Authenticate = Blueprint('Authenticate', __name__, )
import os.path


def _get_public_key():
    public_key = None
    with open(app.config.get('APP_INSTANCE_PEM'), 'rb') as f:
        public_key = f.read()
    return public_key


@Authenticate.route("/authenticate", methods=['POST'])
def login():
    """
    Sjekk med persons/merged først før man lager ny!
    id in [i['id'] for i in d] der d= _items[0]
    :return:
    """
    username = None
    password = None
    token_valid = False

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
            token_valid = True

            # melwin_id or person_id
            person_id = decoded_token.get('person_id', None)

            if person_id is None:
                eve_abort(401, 'Could not validate the token, could not find username')
            else:
                #  print('Username', person_id)
                _user = User(int(person_id), app)

        except jwt.exceptions.InvalidTokenError:
            token_valid = False
            eve_abort(401, 'Could not validate the token, InvalidTokenError')
        except jwt.exceptions.InvalidSignatureError:
            token_valid = False
            eve_abort(401, 'Could not validate the token, InvalidSignatureError')
        except jwt.exceptions.InvalidIssuerError:
            token_valid = False
            eve_abort(401, 'Could not validate the token, InvalidIssuerError')
        except jwt.exceptions.ExpiredSignatureError:
            token_valid = False
            eve_abort(401, 'Could not validate the token, ExpiredSignatureError')
        except Exception as e:
            token_valid = False
            eve_abort(401, 'Could not validate your token {}'.format(e))
    else:
        eve_abort(401, 'Could not make sense of your request')

    # Now process user and successful authentication
    if token_valid is True and _user.user is not None:
        """
        This is where one needs to verify if person has been merged!!
        If merged then lookup like {'id': {'$in': [all_person_ids]}} and then find the person_id used here
        THEN update global, blinker signal 'person-merged'?
        """

        # token = uuid5(uuid4(),rq['username'])
        token = uuid4().hex

        # valid = utc.replace(hours=+2)  # @bug: utc and cet!!!
        # utc = datetime.utcnow() #arrow.utcnow()

        valid = datetime.utcnow() + timedelta(seconds=app.config['AUTH_SESSION_LENGHT'])

        # utc.shift(seconds=+app.config['AUTH_SESSION_LENGHT'])
        # Pure datetime
        # valid = datetime.now() + datetime.timedelta(seconds=60)

        try:
            acl_status, acl = lungo.get_person_acl(_user.person_id)
            if acl_status is False:
                acl = []
            response, _, _, status = patch_internal(resource='users_auth',
                                                    payload={'auth': {'token': token,
                                                                      'valid': valid},  # Arrow utc.datetime
                                                             'acl': [{'activity': a['activity'],
                                                                      'org': a['org'],
                                                                      'role': a['role']
                                                                      } for a in acl],
                                                             },
                                                    concurrency_check=False,
                                                    **{'id': _user.person_id})

            if status in [200, 201]:
                t = '%s:' % token
                b64 = b64encode(t.encode('utf-8'))
                _, activities = lungo.get_person_activities(_user.person_id)
                return eve_response(data={'success': True,
                                          'username': _user.person_id,
                                          'token': token,
                                          'token64': b64.decode('utf-8'),
                                          'valid': valid,
                                          'activities': activities,
                                          'acl': acl,
                                          '_id': str(_user.user.get('_id')),
                                          '_etag': _user.user.get('_etag', None),
                                          'settings': _user.user.get('settings', {})},
                                    status=200)
            else:
                app.logger.error("Could not insert token for %i" % _user.user.get('id'))

        except Exception as e:
            app.logger.exception("Could not update user %s auth token:" % _user.person_id)
            app.logger.exception(e)
            eve_abort(500, "Could not update user %i auth token" % _user.person_id)

    # On error sleep a little against brute force
    sleep(1)

    return eve_response(data={'success': False,
                              'username': None,
                              'token': None,
                              'token64': None,
                              'valid': None,
                              'activities': [],
                              'acl': [],
                              'settings': None,
                              '_id': None,
                              '_etag': None,
                              'message': 'Wrong username or password'},
                        status=200)


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
