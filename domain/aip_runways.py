RESOURCE_COLLECTION = 'aip_runways'
BASE_URL = 'aip/runways'

_schema = {'id': {'type': 'integer',
                  'unique': True,
                  'required': True,
                  },
           'icao': {'type': 'string',
                    'required': True},
           'length': {'type': 'number'},
           'width': {'type': 'number'},
           'surface': {'type': 'string'},
           'lighted': {'type': 'boolean'},
           'closed': {'type': 'boolean'},
           'headings': {'type': 'list',
                        'schema': {'type': 'integer'}
                        },
           'le_ident': {'type': 'string'},
           'le_displaced_threshold': {'type': 'number'},
           'le_heading': {'type': 'integer'},
           'le_height': {'type': 'integer'},
           'he_ident': {'type': 'string'},
           'he_displaced_threshold': {'type': 'number'},
           'he_heading': {'type': 'integer'},
           'he_height': {'type': 'integer'},
           'geo': {'type': 'linestring'}
           }

definition = {
    'item_title': 'Runways',
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
                      'headings': ([('headings', 1)], {'background': True}),
                      'misc': ([('lighted', 1), ('surface', 1), ('length', 1), ('closed', 1)], {'background': True}),
                      'geo': ([('geo', '2dsphere')], {'background': True}),
                      },

    'schema': _schema

}
