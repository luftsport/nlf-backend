from _base import acl_item_schema

RESOURCE_COLLECTION = 'notifications'
BASE_URL = 'notifications'

"""
    "title": "Test 1",
    "msg": "Dette er en testmelding til deg som er vakent..."
    "template": "email",
    "delivered": False,
    "read": False,
    "status": "Pending",
    "channel": "email",
    "from": "fallskjerm_observations",
    "from_id": 46,
    "from_who": 301041,

type: [notification, message, chat, transition, reminder...]
data: { title, msg, template ....} # data packet with everything needed for the various packets 
recepient # who to send to
dismissable
dismissed
transport: None => ikke rapportert!!

transport # email, sms, socket, http
status # 
from
from_id
from_who
created
event_id
acl? - samme som der det ble gjennomført??

SEND IMMEDIATELY, AAGGREGATE OSV??

Getting because why??
why: {reason_type: function, reason_type_id: 26578, reason: 'Hovedinstruktør'}

Saved observation:
title: saved
msg: Einar Huseby did save the observation
current: 13
previous: 12

"""
_schema = {'type': {'type': 'string',
                    'required': True,
                    },
           'data': {'type': 'dict'},  # what, when, where, who, how
           'recepient': {'type': 'int'},
           'sender': {'type': 'int'},
           'event_id': {'type': 'string'},
           'event_created': {'type': 'datetime'},
           'event_from': {'type': 'string'},  # ex motorfly_observations
           'event_from_id': {'type': 'string'},  # ex motorfly observations id....
           'dismissable': {'type': 'boolean'},
           'dismissed': {'type': 'datetime'},
           'transport': {'type': 'string'},  # ['email', 'sms', socket',...]
           'status': {'type': 'string'}, # created, pending, finished

           'acl': acl_item_schema
           }

definition = {
    'item_title': 'content',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   },
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],
    'mongo_indexes': {
        'housekeeping': ([('type', 1), ('dismissable', 1), ('dismissed', 1), ('transports', 1)], {'background': True}),
        'recepients': ([('recepients', 1)], {'background': True}),
    },
    'schema': _schema

}
