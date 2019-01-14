"""

    Melwin memberships
    ==================
    
    Connects the melwin code for membership with human readable description
    
    "_id" : ObjectId("54970947a01ed2381196c9f5"),
    "name" : "Familie Medlemsskap",
    "id" : "FAM"
    
"""
RESOURCE_COLLECTION = 'legacy_melwin_membership'
BASE_URL = 'legacy/melwin/membership'

_schema = {
    'id': {'type': 'string',
           'required': True,
           },
    'name': {'type': 'string',
             },
}

definition = {
    'item_title': 'membership',
    # 'item_url': 'clubs',

    'description': 'Melwin passthrough',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   'default_sort': [('id', 1)],
                   },

    'resource_methods': ['GET'],
    'item_methods': ['GET'],

    'versioning': False,

    'additional_lookup': {
        'url': 'regex("[\w{3}]+")',
        'field': 'id',
    },
    'mongo_indexes': {'id': ([('id', 1)], {'background': True}),
                      'name': ([('name', 1)], {'background': True}),
                      },

    'schema': _schema,
}
