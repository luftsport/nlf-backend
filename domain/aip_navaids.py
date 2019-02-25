RESOURCE_COLLECTION = 'aip_navaids'
BASE_URL = 'aip/navaids'

_schema = {'id': {'type': 'integer',
                  'unique': True,
                  'required': True,
                  },
           'icao': {'type': 'string',
                    'required': True},
           'ident': {'type': 'string'},
           'name': {'type': 'string'},
           'type': {'type': 'string'},
           'frequency': {'type': 'float'},
           'location': {'type': 'point'},
           'dme_channel': {'type': 'string'},
           'dme_frequency': {'type': 'number'},
           'dme_location': {'type': 'point'},
           'slaved_variation': {'type': 'number'},
           'magnetic_variation': {'type': 'number'},
           'power': {'type': 'string'},
           }

definition = {
    'item_title': 'Navaids',
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
                      'stuff': ([('ident', 1), ('type', 1), ('name', 1)], {'background': True}),
                      'location': ([('location', '2dsphere'), ('dme_location', '2dsphere')], {'background': True}),
                      },

    'schema': _schema

}
