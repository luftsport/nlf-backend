"""

    license
    =======
    
    Should return an object with license information
    
    {
        "_id" : ObjectId("5360ad6712afba95dd35a527"),
        "id" : 9,
        "melwinId" : "F-C",
        "licenseName" : "C-lisens",
        "active" : true
    }

"""
RESOURCE_COLLECTION = 'legacy_licenses'
BASE_URL = 'legacy/licenses'

_schema = {
    'id': {'type': 'string',
           'required': True,
           'readonly': True
           },
    'name': {'type': 'string',
             },
    'active': {'type': 'boolean',
               },

    'url': {'type': 'string', 'required': False},
}

definition = {
    'item_title': 'licenses',
    'description': 'Licenses with added snacks',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   'default_sort': [('id', 1)],
                   },
    'extra_response_fields': ['id'],
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'PUT'],

    'versioning': True,

    'additional_lookup': {
        'url': 'regex("[\w{1}\-\w{1,5}]+")',
        'field': 'id',
    },
    'mongo_indexes': {'id': ([('id', 1)], {'background': True}),
                      'name': ([('name', 1)], {'background': True}),
                      },

    'schema': _schema,
}
