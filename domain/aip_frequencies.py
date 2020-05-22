RESOURCE_COLLECTION = 'aip_frequencies'
BASE_URL = 'aip/frequencies'

_schema = {'id': {'type': 'integer',
                  'required': True,
                  'unique': True
                  },
           'icao': {'type': 'string',
                     'required': True,
                     },
           'type': {'type': 'string'},
           'description': {'type': 'string'},
           'frequency': {'type': 'float'},
           }

definition = {
    'item_title': 'Aip Frequencies',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },

    'additional_lookup': {
        'url': 'regex("[A-Za-z]+")',
        'field': 'icao',
    },
    'extra_response_fields': ['icao'],
    'versioning': False,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],

    'pagination_strategy': '',
    'mongo_indexes': {'icao': ([('icao', 1)], {'background': True}),
                      'frequency': ([('frequency', 1), ('type', 1)], {'background': True}),
                      },

    'schema': _schema

}
