RESOURCE_COLLECTION = 'aircrafts'
BASE_URL = 'aircrafts'

_schema = {
    'callsign': {'type': 'string',
                 'required': True,
                 },
    'manufacturer': {'type': 'string'},
    'model': {'type': 'string'},
    'msn': {'type': 'string'},
    'status': {'type': 'string'},
    'type': {'type': 'string'},
    'image': {'type': 'media'}
}

definition = {
    'item_title': 'Aircrafts',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },

    'additional_lookup': {
        'url': 'regex("[\w{2}\-\w{4}]+")',
        'field': 'callsign',
    },
    'extra_response_fields': ['callsign'],
    'versioning': False,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],

    'pagination_strategy': '',
    'mongo_indexes': {'callsign': ([('callsign', 1)], {'background': True}),
                      'misc': ([('manufacturer', 1), ('model', 1), ('type', 1), ('status', 1)], {'background': True}),
                      },

    'schema': _schema

}
