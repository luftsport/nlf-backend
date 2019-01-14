"""

    Users Auth
    ==========
    
    Internal 
    
    Do NOT contain any personal information
    
"""
RESOURCE_COLLECTION = 'users_auth'
BASE_URL = 'internal only'

_schema = {  # Medlemsnummer
    'id': {'type': 'integer',
           'required': True,
           },

    # Acl list of groups and roles
    'acl': {'type': 'dict', },

    'auth': {'type': 'dict',
             'schema': {'token': {'type': 'string'},
                        'valid': {'type': 'datetime'},
                        }
             },

    'user': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'users',
            'field': '_id',
            'embeddable': True,
        },
    },

}

definition = {
    'item_title': 'user auth',

    'internal_resource': True,
    'datasource': {'source': RESOURCE_COLLECTION,
                   'default_sort': [('id', 1)],
                   },

    'resource_methods': [],
    'item_methods': [],

    'versioning': False,

    'additional_lookup': {
        'url': 'regex("[\d{1,6}]+")',
        'field': 'id',
    },
    'mongo_indexes': {'person id': ([('id', 1)], {'background': True}),
                      'acl': ([('acl', 1)], {'background': True}),
                      'auth': ([('auth', 1)], {'background': True}),
                      'user': ([('user', 1)], {'background': True}),
                      },
    'schema': _schema,
}
