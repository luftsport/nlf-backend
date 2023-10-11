RESOURCE_COLLECTION = 'legacy_clubs'
BASE_URL = 'legacy/clubs'

_schema = {
    'id': {'type': 'integer',
           'required': True,
           #'readonly': True
           },
    'club': {'type': 'integer',
             'required': True,
             #'readonly': True
             },
    'name': {'type': 'string',
             },
    'active': {'type': 'boolean',
               },
    'org': {'type': 'string',
            },
    'locations': {'type': 'list'},  # Should be refs or embedded locations??
    'planes': {'type': 'dict'},  # Should be refs or embedded planes??
    'roles': {'type': 'dict'},  # Should be refs or embedded roles
    'ot': {'type': 'integer',
           'required': True,
           'allowed': [1, 2]},
    'ci': {'type': 'integer', 'required': False},  # Embedded or??
    'logo': {'type': 'media', 'required': False},
    'url': {'type': 'string', 'required': False},
    'owner': {'type': 'integer'}
}

definition = {
    'item_title': 'club',
    'description': 'Legacy clubs with added data',

    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   'default_sort': [('id', 1)],
                   },
    'extra_response_fields': ['id'],

    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'PUT'],

    'versioning': True,

    # Make lookup on club id from melwin
    'additional_lookup': {
        'url': 'regex("[\d{1,9}]+")',  # 'url': 'regex("[\d{3}\-\w{1}]+")',
        'field': 'id',
    },
    'mongo_indexes': {'id': ([('id', 1)], {'background': True}),
                      'name': ([('name', 1)], {'background': True}),
                      },
    'schema': _schema,
}
