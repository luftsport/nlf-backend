"""

    Acl groups
    ==========
    
    
"""
RESOURCE_COLLECTION = 'acl_groups'
BASE_URL = 'acl/groups'

_schema = {'name': {'type': 'string',
                    'required': 'true',
                    'unique': True},
           'description': {'type': 'string'},
           'ref': {'type': 'string',
                   'unique': True
                   },

           }

definition = {
    'item_title': 'acl_groups',
    'item_name': 'acl_groups',

    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   },
    'allowed_write_roles': ['superadmin'],
    'allowed_item_write_roles': ['superadmin'],
    'internal_resource': False,
    'concurrency_check': True,

    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],

    'versioning': False,

    'additional_lookup': {
        'url': 'regex("[\d{3}\-\w{1}]+")',
        'field': 'ref',
    },

    'mongo_indexes': {'name': ([('name', 1)], {'background': True}),
                      'ref': ([('ref', 1)], {'background': True}),
                      },

    'schema': _schema,
}
