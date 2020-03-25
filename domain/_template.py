"""

    Template for definitions
    ========================
    
    @summary: A simple template for definitions, copy paste 
    
    @see:     Confluence Eve help url
    @todo:    Add all config options
    
"""

RESOURCE_COLLECTION = ''
BASE_URL = ''

_schema = {
            '': {'type': 'string',
                 'required': True,
                 },
           
            '': {'type': 'dict',
                 'required': True,
                 },
                
            }

definition = {

    'url': BASE_URL,
    'item_title': 'The title for doc etc',
    'datasource': {'source': RESOURCE_COLLECTION,
                   },

    'additional_lookup': {
        'url': 'regex("[\d{1,9}]+")',
        'field': 'id',
    },
    'extra_response_fields': ['id'],

    'versioning': True,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],

    'mongo_indexes': {'name of index': ([('field', 1)], {'background': True}),
                      'location': ([('address.location.geo', '2dsphere')], {'background': True}),
                      'full text': ([('full_name', 'text')], {'background': True})
                      },
    'schema': _schema
}