"""

    Acl roles
    =========
    
    
"""
RESOURCE_COLLECTION = 'acl_roles'
BASE_URL = 'acl/roles'

_schema = {'name': {'type': 'string',
                    'required': 'true',
                    },
           'description': {'type': 'string'},
           'ref': {'type': 'string',
                   'unique': True},
           'group': {
               'type': 'objectid',
               'required': True,
               'data_relation': {
                   'resource': 'acl/groups',
                   'field': '_id',
                   'embeddable': True,
               },
           },

           }

definition = {
    'item_title': 'acl/roles',
    'url': BASE_URL,
    'allowed_write_roles': ['superadmin'],
    'allowed_item_write_roles': ['superadmin'],
    'datasource': {'source': RESOURCE_COLLECTION,
                   },
    'internal_resource': False,
    'concurrency_check': True,

    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],

    'versioning': False,

    'mongo_indexes': {'name': ([('name', 1)], {'background': True}),
                      'ref': ([('ref', 1)], {'background': True}),
                      'group': ([('group', 1)], {'background': True}),
                      },

    'schema': _schema,
}
