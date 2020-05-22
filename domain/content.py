from _base import acl_item_schema

RESOURCE_COLLECTION = 'content'
BASE_URL = 'content'

_schema = {'title': {'type': 'string',
                     'required': True,
                     'readonly': False
                     },
           'slug': {'type': 'string',
                    'required': True},
           'body': {'type': 'string',
                    'required': True},
           'space_key': {'type': 'string',
                         'required': True},
           'parent': {'type': 'objectid',
                      'nullable': True,
                      'default': None},
           'order': {'type': 'integer'},
           'ref': {'type': 'string'},
           'owner': {'type': 'integer',
                     'required': False,
                     'readonly': True},
           'published': {'type': 'boolean'},
           'acl': acl_item_schema
           }

definition = {
    'item_title': 'content',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },
    'additional_lookup': {
        'url': 'regex("[a-z0-9-]+")',
        'field': 'slug',
    },
    'extra_response_fields': ['key'],
    'versioning': True,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'mongo_indexes': {'slug': ([('slug', 1)], {'background': True}),
                      'space': ([('space_key', 1)], {'background': True}),
                      'parent': ([('parent', 1)], {'background': True}),
                      'acl': ([('acl', 1)], {'background': True}),
                      'published': ([('published', 1)], {'background': True}),
                      'owner': ([('owner', 1)], {'background': True}),
                      'content': ([('title', 'text'), ('body', 'text')], {'background': True})
                      },
    'schema': _schema

}
