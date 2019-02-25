
RESOURCE_COLLECTION = 'aip_airspace'
BASE_URL = 'aip/airspaces'

_limit = {'altitude': {'type': 'integer'},
          'reference': {'type': 'string'},
          'unit': {'type': 'string'}}

_schema = {'id': {'type': 'integer',
                  'unique': True,
                  'required': True,
                  },
           'name': {'type': 'string'},
           'version': {'type': 'string'},
           'country': {'type': 'string'},
           'category': {'type': 'string'},
           'type': {'type': 'string'},
           'altlimit_bottom': {'type': 'dict', 'schema': _limit},
           'altlimit_top': {'type': 'dict', 'schema': _limit},
           'geometry': {'type': 'polygon'}
           }

definition = {
    'item_title': 'Airspaces',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },

    'additional_lookup': {
        'url': 'regex("[A-Za-z]+")',
        'field': 'id',
    },
    'extra_response_fields': ['id'],
    'versioning': False,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],

    'pagination_strategy': '',
    'mongo_indexes': {'ident': ([('id', 1)], {'background': True}),
                      'category': ([('category', 1), ('type', 1)], {'background': True}),
                      'iso': ([('country', 1)], {'background': True}),
                      'geo': ([('geometry', '2dsphere')], {'background': True}),
                      'name': ([('name', 'text')], {'background': True})
                      },

    'schema': _schema

}