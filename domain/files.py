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
           'last_modified': {'type': 'datetime'},
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
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'versioning': False,
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

"""
Find duplicate files by md5 sum
"""
agg_duplicate_files = {
    'url': 'files/duplicates',
    'item_title': 'Duplicate files',
    'pagination': True,
    'datasource': {
        'source': 'fs.files',
        'aggregation': {
            'pipeline': [
                {
                    "$group": {
                        "_id": "$md5",
                        "num": {
                            "$sum": 1
                        },
                        "ref_ids": {"$addToSet": "$_id"},
                        "length": {"$sum": "$length"},
                        "content_type": {"$first": "$contentType"}
                    }
                },
                {
                    "$match": {
                        "num": {
                            "$gt": 1
                        }
                    }
                }

            ]
        }
    }
}

"""
Find orphan files
"""
agg_orphan_files = {
    'url': 'files/orphan',
    'item_title': 'Orphan files',
    'pagination': True,
    'datasource': {
        'source': 'fs.files',
        'aggregation': {
            'pipeline': [
                {
                    "$lookup": {
                        "from": "files",
                        "localField": "_id",
                        "foreignField": "file",
                        "as": "refs"
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "uploadDate": 1,
                        "contentType": 1,
                        "length": 1,
                        "md5": 1,
                        "ref_count": {
                            "$size": "$refs"
                        }
                    }
                },
                {
                    "$match": {
                        "ref_count": 0
                    }
                }

            ]
        }
    }
}
