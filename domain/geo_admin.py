RESOURCE_COLLECTION = 'geo_admin'
BASE_URL = 'geo/admin'

_schema = {
    'name': {'type': 'string',
             'required': True},
    'id': {'type': 'integer'},
    'local_id': {'type': 'integer'},
    'type': {'type': 'string',
             'required': True,
             },
    'country': {'type': 'string',
                'required': True,
                },
    'geometry': {'type': 'dict'},
    'e5x': {'type': 'integer'}
}

definition = {
    'item_title': 'Geojson Administrative Areas Definitions',
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
                      'type': ([('type', 1)], {'background': True}),
                      'geometry': ([('geometry', '2dsphere')], {'background': True}),
                      },

    'schema': _schema

}
