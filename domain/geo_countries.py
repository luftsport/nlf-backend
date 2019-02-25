RESOURCE_COLLECTION = 'geo_countries'
BASE_URL = 'geo/countries'

_schema = {
           'name': {'type': 'string',
                    'required': True},
           'iso': {'type': 'string',
                   'required': True,
                   },
           'geometry': {'type': 'dict'},
           }

definition = {
    'item_title': 'Geojson Countries Definitions',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },

    'additional_lookup': {
        'url': 'regex("[A-Za-z]+")',
        'field': 'name',
    },
    'extra_response_fields': ['name'],
    'versioning': False,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],

    'pagination_strategy': '',
    'mongo_indexes': {'name': ([('name', 1)], {'background': True}),
                      'iso': ([('iso', 1)], {'background': True}),
                      'geometry': ([('geometry', '2dsphere')], {'background': True}),
                      },

    'schema': _schema

}
