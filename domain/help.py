from _base import acl_item_schema

RESOURCE_COLLECTION = 'help'
BASE_URL = 'help'

_schema = {'key': {'type': 'string',
                   'required': True,
                   'readonly': False,
                   'unique': True
                   },
           'title': {'type': 'string',
                     'required': True},
           'body': {'type': 'string'},
           'owner': {'type': 'integer'},
           'acl': acl_item_schema
           }

definition = {
    'item_title': 'help',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },

    'additional_lookup': {
        'url': 'regex("[a-z-]+")',
        'field': 'key',
    },
    'extra_response_fields': ['key'],
    'versioning': True,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],

    'mongo_indexes': {'key': ([('key', 1)], {'background': True}),
                      'owner': ([('owner', 1)], {'background': True}),
                      'acl': ([('acl', 1)], {'background': True}),
                      'content': ([('title', 'text'), ('body', 'text')], {'background': True})
                      },

    'schema': _schema

}
