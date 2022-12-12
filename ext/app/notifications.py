from flask import g, current_app as app
from eve.methods.post import post_internal
import datetime
from uuid import uuid4
import re

# Broadcast socketio
from ext.app.responseless_decorators import _async
import socketio
import time

from ext.app.lungo import get_recepients, get_recepients_from_roles, get_users_from_role

RESOURCE_COLLECTION = 'notifications'


'''
OBSREG:
ors_workflow
ors_save 
ors_acl
ors_reminder
ors_message
'''


@_async
def broadcast(message):
    try:
        sio = socketio.Client()
        sio.connect('http://localhost:8080?token=tulletoken')
        sio.emit('broadcast', message)
        time.sleep(0.1)
        sio.disconnect()
    except:
        pass


class Notification:

    def __init__(self, event_from, event_from_id, event_type, dismissable=True, acl={}):
        self.event_data = {
            'event_id': str(uuid4()),
            'type': event_type,
            'recepient': None,  # person_id
            'sender': g.user_id,  # person_id
            'event_from': event_from,  # collection
            'event_from_id': event_from_id,  # Document _id or id
            'event_created': datetime.datetime.utcnow(),
            'dismissable': dismissable,  # can be dismissed by recepient?
            'dismissed': False,
            'transport': 'email',  # transports are email, sms, socket, None
            'transport_mode': 'immediate',  # immediate, aggregate, aggregate_5m, aggregate_1d osv transport_delay 0 10
            'status': 'ready',  # ready, pending, finished
            'data': {},  # custom data packet adapted to which...
            # 'acl': acl  # the acl for this very notification?
        }

    def _create(self, payload):

        if 'comment' in payload.get('data', {}) and payload['data']['comment'] is None:
            payload['data']['comment'] = ''

        payload['uuid'] = str(uuid4())

        response, _, _, return_code, location_header = post_internal('notifications', payload)
        if return_code == 201:
            return True, response

        return False, {}

    def notify_person(self, person_id, data):
        event_data = self.event_data.copy()
        event_data['recepient'] = person_id
        event_data['data'] = data
        return self._create(event_data)

    def notify_all(self, recepients, data):
        if type(recepients) is list:
            for person_id in recepients:
                self.notify_person(person_id, data)
        else:
            self.notify_person(recepients, data)


# Specific
def ors_housekeeping(recipients, event_type, event_from, event_from_id, message, ors_id, org_id, ors_tags):
    n = Notification(event_from=event_from, event_from_id=event_from_id, event_type=event_type,
                     dismissable=True, acl={})

    data = {
        'id': ors_id,
        'tags': ors_tags,
        'org_id': org_id,
        'action': 'notify',
        'context': 'housekeeping',
        'message': message
    }

    n.notify_all(recipients, data)
def ors_message(recepients, event_from, event_from_id, message, ors_id, org_id, ors_tags):
    n = Notification(event_from=event_from, event_from_id=event_from_id, event_type='ors_message',
                     dismissable=True, acl={})

    data = {
        'id': ors_id,
        'tags': ors_tags,
        'org_id': org_id,
        'message': message
    }

    n.notify_all(recepients, data)


def ors_reminder(recepients, event_from, event_from_id, ors_id, org_id, ors_tags):
    n = Notification(event_from=event_from, event_from_id=event_from_id, event_type='ors_reminder',
                     dismissable=True, acl={})

    data = {
        'id': ors_id,
        'tags': ors_tags,
        'org_id': org_id,
    }

    n.notify_all(recepients, data)


def ors_acl(recepients, event_from, event_from_id, right, verb, ors_id, org_id, ors_tags):
    n = Notification(event_from=event_from, event_from_id=event_from_id, event_type='ors_acl',
                     dismissable=True, acl={})
    data = {
        'id': ors_id,
        'tags': ors_tags,
        'org_id': org_id,
        'right': right,
        'verb': verb
    }
    n.notify_all(recepients, data)


def ors_workflow(recepients, event_from, event_from_id, ors_id, org_id, ors_tags, action, source, destination, comment,
                 context='transition'):
    n = Notification(event_from=event_from, event_from_id=event_from_id, event_type='ors_workflow',
                     dismissable=True, acl={})

    data = {
        'id': ors_id,
        'tags': ors_tags,
        'org_id': org_id,
        'action': action,
        'comment': comment,
        'source': source,
        'destination': destination,
        'context': context
    }
    n.notify_all(recepients, data)


def ors_save(recepients, event_from, event_from_id, source, destination, context='save'):
    n = Notification(event_from=event_from, event_from_id=event_from_id, event_type='ors_save',
                     dismissable=True, acl={})

    n.event_data['transport'] = 'socket'
    n.event_data['transport_mode'] = 'aggregate'

    data = {
        'action': 'save',
        'source': source,
        'destination': destination,
        'context': context
    }
    n.notify_all(recepients=recepients, data=data)


def ors_e5x(recepients, event_from, event_from_id, source, ors_id, ors_tags, status, file_name, transport='sftp',
            context='send'):
    n = Notification(event_from=event_from, event_from_id=event_from_id, event_type='ors_e5x',
                     dismissable=True, acl={})

    data = {
        'id': ors_id,
        'tags': ors_tags,
        'action': 'save',
        'source': source,
        'status': status,
        'file_name': file_name,
        'transport': transport,
        'context': context
    }
    n.notify_all(recepients=recepients, data=data)


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
