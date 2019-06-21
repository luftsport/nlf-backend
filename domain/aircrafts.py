RESOURCE_COLLECTION = 'aircrafts'
BASE_URL = 'aircrafts'

_schema = {
    'callsign': {'type': 'string',
                 'required': True,
                 'unique': False
                 },
    'manufacturer': {'type': 'string'},
    'model': {'type': 'string'},
    'msn': {'type': 'string'},
    'status': {'type': 'string'},
    'type': {'type': 'string'},
    'image': {'type': 'string'}, #'media'},
    'e5x': {'type': 'dict'},
    'comment': {'type': 'string'},
    'weight': {'type': 'integer'},
    'engines': {'type': 'integer'},
    'mmsi': {'type': 'string'},
    'nkom': {'type': 'dict'},
    'updated_by': {'type': 'integer'}
    
}

definition = {
    'item_title': 'Aircrafts',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   #'projection': {'image': 0}
                   },

    'additional_lookup': {
        'url': 'regex("[\w{2}\-\w{4}]+")',
        'field': 'callsign',
    },
    'extra_response_fields': ['callsign'],
    'versioning': True,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],
    'allow_unknown': True, # To allow search?
    'pagination_strategy': 'estimated',
    'mongo_indexes': {'callsign': ([('callsign', 1)], {'background': True}),
                      'person': ([('updated_by', 1)], {'background': True}),
                      'misc': ([('manufacturer', 1), ('model', 1), ('type', 1), ('status', 1)], {'background': True}),
                      'txt': ([('callsign', 'text'), ('manufacturer', 'text'), ('model', 'text')], {'background': True, 'default_language': 'norwegian', 'weights': {'callsign': 10, 'manufacturer': 4, 'model': 2}})
                      },

    'schema': _schema

}


# Aggregation
from bson import SON, ObjectId

agg_count_types = {
    'url': 'aircrafts/types',
    'item_title': 'Aircraft Types Count',
    'pagination': False,
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$group": {"_id": {"type": "$type"}, "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1), ("_id", -1)])}
            ]
        }
    }
}
