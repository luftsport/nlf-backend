"""

    Melwin licenses
    ===============
    
    Should return an object with license information
    

"""
RESOURCE_COLLECTION = 'legacy_melwin_licenses'
BASE_URL = 'legacy/melwin/licenses'

_schema = {
    'id': {'type': 'string',
           'required': True,
           },
    'name': {'type': 'string',
             },
}

definition = {
    'item_title': 'Legacy Melwin licenses',
    # 'item_url': 'clubs',
    'url': BASE_URL,
    'description': 'Melwin passthrough',

    'datasource': {'source': RESOURCE_COLLECTION,
                   'default_sort': [('id', 1)],
                   },

    'resource_methods': ['GET'],
    'item_methods': ['GET'],

    'versioning': False,

    'additional_lookup': {
        'url': 'regex("[\w{1}\-\w{1,5}]+")',
        'field': 'id',
    },
    'mongo_indexes': {'id': ([('id', 1)], {'background': True}),
                      'name': ([('name', 1)], {'background': True}),
                      },

    'schema': _schema,
}
