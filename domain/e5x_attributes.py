RESOURCE_COLLECTION = 'e5x_attributes'
BASE_URL = 'e5x/attributes'

_schema = {
    'attribute': {'type': 'string'},
    'attribute_id': {'type': 'integer'},
    'parent_id': {'type': 'integer', 'nullable': True},
    'datatype': {'type': 'integer', 'nullable': True},
    'default': {'type': 'integer', 'nullable': True},
    'special_attribute_id': {'type': 'integer', 'nullable': True},
    'min': {'type': 'integer', 'nullable': True},
    'max': {'type': 'integer', 'nullable': True},
    'choices_key': {'type': 'string', 'nullable': True},
    'type': {'type': 'string', 'nullable': True},
    'restrictions': {'type': 'dict', 'nullable': True},
    'rit_version': {'type': 'string'}
}

definition = {
    'item_title': 'E5X Attributes',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   },
    'additional_lookup': {
        'url': 'regex("[a-z.0-9-]+")',
        'field': 'attribute',
    },
    'extra_response_fields': ['attribute'],
    'versioning': False,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'mongo_indexes': {'attr': ([('attribute', 1)], {'background': True}),
                      'content': ([('attribute', 'text')], {'background': True}),
                      'rit_version': ([('rit_version', 1)], {'background': True})
                      },
    'schema': _schema

}
