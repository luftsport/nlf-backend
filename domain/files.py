"""

    Files:
    ======
    
    Files are references in current document, and when loaded they output a base64 encoded string
    
    Use ?projection={"files": 0} to _not_ load files directly
    
"""

from _base import acl_item_schema

RESOURCE_COLLECTION = 'files'
BASE_URL = 'files'

_schema = {'name': {'type': 'string'},
           'description': {'type': 'string'},
           'tags': {'type': 'list'},
           'content_type': {'type': 'string'},
           'size': {'type': 'integer'},
           'owner': {'type': 'integer'},
           'ref': {'type': 'string', 'required': True},  # say observations
           'ref_id': {'type': 'objectid', 'required': True},  # say ObjectId(545bda27a01ed25c57a10ad0) maybe a db ref?
           'file': {'type': 'media', 'required': True},  # Now, this is just a bunch of references is it?
           'activity': {'type': 'string'},
           'acl': acl_item_schema,
           }

definition = {

    'item_title': 'Files',

    'description': 'Universal file storage and retrieval',
    'url': BASE_URL,
    'datasource': {
        'source': RESOURCE_COLLECTION,
        # 'projection': {'file': 1}
    },
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],
    'versioning': True,
    'mongo_indexes': {'name': ([('slug', 1)], {'background': True}),
                      'tags': ([('tags', 1)], {'background': True}),
                      'content': ([('content_type', 1)], {'background': True}),
                      'ref': ([('ref', 1), ('ref_id', 1)], {'background': True}),
                      'owner': ([('owner', 1)], {'background': True}),
                      'acl': ([('acl', 1)], {'background': True}),
                      'descr': ([('description', 'text'), ('name', 'text')], {'background': True})
                      },
    'schema': _schema,

}
