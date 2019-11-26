"""
    Observation Workflow Controller
    ===============================

    Model: ext.workflows.observation.ObservationWorkflow

    @todo: Signals on change signal to communications to dispatch an update to the watchers
           http://stackoverflow.com/questions/16163139/catch-signals-in-flask-blueprint

"""
from flask import Blueprint, current_app as app, request  # , Response, abort, jsonify, make_response
import base64
import uuid
import datetime
# Need custom decorators
from ext.app.decorators import *
from ext.app.eve_helper import eve_response, eve_response_pppd

from ext.app.lungo import get_orgs_in_activivity, get_users_from_role
from eve.methods.post import post_internal
from eve.methods.patch import patch_internal
from eve.methods.get import getitem_internal, get_internal

from ext.auth.acl import get_acl, parse_acl
from bson import ObjectId
import re

import requests
from ext.scf import LUNGO_HEADERS, LUNGO_URL

Notifications = Blueprint('Notifications', __name__, )

RESOURCE_COLLECTION = 'notifications'
REMINDER_DELTA = 3600  # 1 hour?


## Remove xml style tags from an input string.
#
#  @param string The input string.
#  @param allowed_tags A string to specify tags which should not be removed.
def _strip_tags(string, allowed_tags=''):
    if allowed_tags != '':
        # Get a list of all allowed tag names.
        allowed_tags_list = re.sub(r'[\\/<> ]+', '', allowed_tags).split(',')
        allowed_pattern = ''
        for s in allowed_tags_list:
            if s == '':
                continue;
            # Add all possible patterns for this tag to the regex.
            if allowed_pattern != '':
                allowed_pattern += '|'
            allowed_pattern += '<' + s + ' [^><]*>$|<' + s + '>|'
        # Get all tags included in the string.
        all_tags = re.findall(r'<]+>', string, re.I)
        for tag in all_tags:
            # If not allowed, replace it.
            if not re.match(allowed_pattern, tag, re.I):
                string = string.replace(tag, '')
    else:
        # If no allowed tags, remove all.
        string = re.sub(r'<[^>]*?>', '', string)

    return string
def strip_tags(string):

    return _strip_tags(re.sub('<br\s*?>', '\n', string))

def _create(payload):
    # resource, payl = None, skip_validation = False
    # response, None, None, return_code, location_header
    response, _, _, return_code, location_header = post_internal('notifications', payload)
    print('CREATED', response, return_code, location_header)
    return response

@Notifications.route("/message", methods=['POST'])
@require_token()
def message():

    try:

        args = request.get_json(force=True)  # use force=True to do anyway!

        event_from = args.get('event_from', None)
        event_from_id = args.get('event_from_id', None)
        message = strip_tags(args.get('message', None))

        if event_from is None or event_from_id is None or message is None:
            eve_abort(422, 'Missing parameters')

        transport = 'email'

        event_type = 'message'
        event_id = str(uuid.uuid4())
        event_created = datetime.datetime.utcnow()

        print(event_from, event_from_id, type(event_created), event_created, '{}'.format(datetime.datetime.utcnow()))

        # Can't do shit if lukket or trukket!
        status, acl = get_acl(event_from, event_from_id, projection={'acl': 1, 'workflow.state': 1})

        if acl.get('workflow', {}).get('state', 'closed') == 'closed':
            return eve_response('Observation is close', 403)

        res = parse_acl(acl)

        k = [p for p in list(set(res['read'] + res['write'] + res['execute'] + res['delete'])) if p != app.globals.get('user_id', 0)]

        # k = res
        for user_id in k:

            # Not to self!
            if user_id != app.globals.get('user_id', None):
                data = {
                    'type': event_type,
                    'recepient': user_id,
                    'sender': app.globals.get('user_id'),
                    'event_id': event_id,
                    'event_from': event_from,
                    'event_from_id': event_from_id,
                    'event_created': event_created,
                    'dismissable': True,
                    'dismissed': None,
                    'transport': transport,
                    'status': 'ready',
                    'data': {
                        'message': message
                    }
                }

                _create(data)

        return eve_response(k, 200)
    except Exception as e:
        print('ERR', e)
        return eve_response({}, 500)


# @Notifications.route("/reminder/<string:app>/<string:activity>/<objectid:_id>", methods=['POST'])
# def notify(app, activity, _id):
@Notifications.route("/reminder", methods=['POST'])
@require_token()
def notify():
    """ Get current state, actions, transitions and permissions
    'type': {'type': 'string',
                    'required': True,
                    },
           'data': {'type': 'dict'},  # what, when, where, who, how
           'recepient': {'type': 'integer'},
           'sender': {'type': 'integer'},
           'event_id': {'type': 'string'},
           'event_created': {'type': 'datetime'},
           'event_from': {'type': 'string'},  # ex motorfly_observations
           'event_from_id': {'type': 'objectid'},  # {'type': 'string'},  # ex motorfly observations id....
           'dismissable': {'type': 'boolean'},
           'dismissed': {'type': 'datetime', 'nullable': True},
           'transport': {'type': 'string'},  # ['email', 'sms', socket',...]
           'status': {'type': 'string'},  # created, pending, finished

    """

    """
    1) Check if has access and if not X
    2) Find the x'es 
    3) make sure sender not an x!! see 1...
    4) make sure we're not trying to notify too soon after last one => get last notification for this x+event_from+event_from_id
    5) find x'es user settings - says something about their transmission preferences (mail, aggregate, sms...)
    6) Notify x'es! or both x and w - with users preferences!
    """
    try:


        args = request.get_json(force=True)  # use force=True to do anyway!

        event_from = args.get('event_from', None)
        event_from_id = args.get('event_from_id', None)

        if event_from is None or event_from_id is None:
            eve_abort(422, 'Missing parameters')

        transport = 'email'

        event_type = 'notification'
        event_id = str(uuid.uuid4())
        event_created = datetime.datetime.utcnow()

        print(event_from, event_from_id, type(event_created), event_created, '{}'.format(datetime.datetime.utcnow()))

        status, acl = get_acl(event_from, event_from_id)
        res = parse_acl(acl)

        k = [p for p in list(set(res['read'] + res['write'] + res['execute'] + res['delete'])) if p != app.globals.get('user_id', 0)]

        print('K', k)
        k.sort()
        print('Ksort', k)
        disapproved_users = get_within_delay(event_from_id, event_type, k) if len(k) > 0 else []
        print('D', disapproved_users)
        disapproved_users.sort()
        print('Dsort', disapproved_users)


        if len(k)==0:
            return eve_response_pppd({'data': 'Fant ingen å sende til'}, 404, 'Found no recepients!')
        
        if disapproved_users == k:
            return eve_response_pppd({'data': 'Please wait for the remaining graceperiod until {}'.format(
                (datetime.datetime.utcnow() - datetime.timedelta(seconds=REMINDER_DELTA))
            )
            },
                429,
                'Too soon to send notification')
        # k = res
        for user_id in k:

            # Not to self!
            if user_id not in disapproved_users and user_id != app.globals.get('user_id', None):
                data = {
                    'type': event_type,
                    'recepient': user_id,
                    'sender': app.globals.get('user_id'),
                    'event_id': event_id,
                    'event_from': event_from,
                    'event_from_id': event_from_id,
                    'event_created': event_created,
                    'dismissable': True,
                    'dismissed': None,
                    'transport': transport,
                    'status': 'ready'
                }

                _create(data)

        return eve_response(k, 200)
    except Exception as e:
        print('ERR', e)
        return eve_response({}, 500)


def get_within_delay(_id, event_type='notification', persons=[] ):
    lookup = {
        'event_from_id': _id,
        'recepient': {'$in': persons},
        'type': event_type,
        'event_created': {'$gte': datetime.datetime.utcnow() - datetime.timedelta(seconds=REMINDER_DELTA)}
    }
    response, _, _, status, _ = get_internal('notifications', **lookup)
    return list(set([notification['recepient'] for notification in response['_items']]))


def generate_event():
    pass





