from bson import ObjectId

RESOURCE_COLLECTION = 'housekeeping'
BASE_URL = 'housekeeping'

_schema = {
    'id': {'type': 'integer'},
    'last_housekeeping': {'type': 'string', 'nullable': True},
    'days_since_last_action': {'type': 'integer'},
    'action': {'type': 'string', 'nullable': True},
    'recipients': {'type': 'list', 'default': []},
    'activity': {'type': 'string'},
    'event_from': {'type': 'string'},
    'event_from_id': {'type': 'objectid'},
    'last_updated': {'type': 'datetime'}
}

definition = {
    'item_title': 'housekeeping',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   },
    'internal_resource': True,
    'allow_unknown': True,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],
    'mongo_indexes': {
        'housekeeping': (
            [('id', 1), ('last_housekeeping', 1), ('action', 1), ('activity', 1), ('event_from', 1),
             ('event_from_id', 1)],
            {'background': True}),
        'recepients': ([('recepients', 1)], {'background': True}),
    },
    'additional_lookup': {
        'url': 'regex("[a-fA-F0-9-]+")',
        'field': 'id',
    },
    'schema': _schema

}
