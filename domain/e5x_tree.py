RESOURCE_COLLECTION = 'e5x_tree'
BASE_URL = 'e5x/tree'

_schema = {

    'name': {'type': 'string'},
    'version': {'type': 'string', 'nullable': True},
    'domain': {'type': 'string', 'nullable': True},
    'Occurrence': {'type': 'dict', 'nullable': True}
}

definition = {
    'item_title': 'E5X Tree',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   },

    'versioning': False,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': _schema

}