RESOURCE_COLLECTION = 'aip_countries'
BASE_URL = 'aip/countries'

_schema = {
           'name': {'type': 'string',
                    'required': True},
           'iso': {'type': 'string'},
           'continent': {'type': 'string'},
           'wikipedia': {'type': 'string'},
           'keywords': {'type': 'string'},
           }

definition = {
    'item_title': 'Geojson Countries Definitions',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },

    'additional_lookup': {
        'url': 'regex("[A-Za-z]+")',
        'field': 'iso',
    },
    'extra_response_fields': ['iso'],
    'versioning': False,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],

    'pagination_strategy': '',
    'mongo_indexes': {'name': ([('name', 1)], {'background': True}),
                      'geo': ([('iso', 1), ('continent', 1)], {'background': True}),
                      },

    'schema': _schema

}
