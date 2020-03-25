RESOURCE_COLLECTION = 'aip_regions'
BASE_URL = 'aip/regions'

_schema = {
    'name': {'type': 'string',
             'required': True},
    'code': {'type': 'string'},
    'local_code': {'type': 'string'},
    'iso_country': {'type': 'string'},
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
        'url': 'regex("[A-Za-z0-9]+")',
        'field': 'code',
    },
    'extra_response_fields': ['code'],
    'versioning': False,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET'],

    'pagination_strategy': '',
    'mongo_indexes': {'name': ([('name', 1)], {'background': True}),
                      'geo': ([('iso_country', 1), ('continent', 1)], {'background': True}),
                      },

    'schema': _schema

}
