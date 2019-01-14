"""

    Melwin Clubs
    ============
    
    Clubs from Melwin
    
"""
RESOURCE_COLLECTION = 'legacy_melwin_clubs'
BASE_URL = 'legacy/melwin/clubs'

_schema = {
    'id': {'type': 'string',
           'required': True,
           },
    'name': {'type': 'string',
             },
}

definition = {
    'item_title': 'club',
    'url': BASE_URL,
    'description': 'Melwin passthrough',

    'datasource': {'source': RESOURCE_COLLECTION,
                   'default_sort': [('id', 1)],
                   },

    'resource_methods': ['GET'],
    'item_methods': ['GET'],

    'versioning': False,

    # Make lookup on club id from melwin
    'additional_lookup': {
        'url': 'regex("[\d{3}\-\w{1}]+")',
        'field': 'id',
    },
    'mongo_indexes': {'id': ([('id', 1)], {'background': True}),
                      'name': ([('name', 1)], {'background': True}),
                      },
    'schema': _schema,
}
