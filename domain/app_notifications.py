from _base import acl_item_schema
from bson import SON, ObjectId
from flask import current_app as app

RESOURCE_COLLECTION = 'notifications'
BASE_URL = 'notifications'

_schema = {'type': {'type': 'string',
                    'required': True,
                    },
           'uuid': {'type': 'string'},
           'data': {'type': 'dict'},  # what, when, where, who, how
           'recepient': {'type': 'integer'},  # Who's the recepient
           'sender': {'type': 'integer'},  #
           'event_id': {'type': 'string'},
           'event_created': {'type': 'datetime'},
           'event_from': {'type': 'string'},  # ex motorfly_observations
           'event_from_id': {'type': 'objectid'},  # {'type': 'string'},  # ex motorfly observations id....
           # 'event_person_id': {'type': 'integer'}, # Sender
           'dismissable': {'type': 'boolean'},  # Can dimiss?
           'dismissed': {'type': 'datetime', 'nullable': True},
           'transport': {'type': 'string'},  # ['email', 'sms', socket',...]
           'transport_mode': {'type': 'string'},  # immediate, aggregate_5m, aggregate_1d osv transport_delay 0 10
           'status': {'type': 'string'},  # created, pending, delivered
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
        'uuid': ([('uuid', 1)], {'background': True}),
        'event': ([('event_from', 1), ('event_from_id', 1), ('event_created', 1)], {'background': True}),
        'recepient': ([('recepient', 1)], {'background': True}),
    },
    'additional_lookup': {
        'url': 'regex("[a-fA-F0-9-]+")',
        'field': 'uuid',
    },
    'schema': _schema

}

# AGGREGATION
agg_events = {
    'url': 'notifications/events',
    'item_title': 'Get notifications by event_from_id and event_from grouped by events',
    'pagination': False,
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {
                    "$match": {
                        "event_from": "$event_from",
                        "event_from_id": "$event_from_id",

                    }
                },

                {
                    "$group": {
                        "_id": "$event_id",
                        "type": {
                            "$first": "$type"
                        },
                        "recepients": {
                            "$addToSet": "$recepient"
                        },
                        "sender": {
                            "$first": "$sender"
                        },
                        "event_created": {
                            "$first": "$event_created"
                        },
                        "dimissed": {
                            "$first": "$dismissed"
                        },
                        "transport": {
                            "$first": "$transport"
                        },
                        "status": {
                            "$first": "$status"
                        },
                        "data": {
                            "$first": "$data"
                        }
                    }
                },
                {"$sort": {"event_created": -1}}  # SON([("data.when", -1)])},

            ]
        }
    }
}
