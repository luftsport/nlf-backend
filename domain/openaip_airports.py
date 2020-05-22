RESOURCE_COLLECTION = 'openaip_airports'
BASE_URL = 'openaip/airports'

_schema = {'icao': {'type': 'string',
                  'required': False,
                  'readonly': False,
                  'unique': True
                  },
           'type': {'type': 'string'},
           'name': {'type': 'string'},
           'country': {'type': 'string'},
           'location': {'type': 'point'},
           'radio': {'type': 'list'},
           'rwy': {'type': 'list'},
           }

definition = {
    'item_title': 'Airports',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },

    'additional_lookup': {
        'url': 'regex("[A-Za-z]+")',
        'field': 'icao',
    },
    'extra_response_fields': ['ident'],
    'versioning': False,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],
    'pagination_strategy': 'none',
    'mongo_indexes': {'icao': ([('icao', 1)], {'background': True}),
                      'country': ([('country', 1)], {'background': True}),
                      'location': ([('location', '2dsphere')], {'background': True}),
                      'name': ([('title', 'text'), ('body', 'text')], {'background': True})
                      },

    'schema': _schema
    }
