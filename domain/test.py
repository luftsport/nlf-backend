from bson import SON
from datetime import datetime

RESOURCE_COLLECTION = 'test'
BASE_URL = 'test'

_schema = {'id': {'type': 'integer',
                  'required': True,
                  },
           'name': {'type': 'string'},
           }

definition = {
    'item_title': 'Eve testing',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0} # Not for this?
                   },

    'additional_lookup': {
        'url': 'regex("[A-Za-z]+")',
        'field': 'id',
    },
    'extra_response_fields': ['id'],
    'versioning': False,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],

    'mongo_indexes': {'id': ([('id', 1)], {'background': True}),
                      'name': ([('name', 'text')], {'background': True})
                      },

    'schema': _schema

}

"""

    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$unwind": "$type"},
                {"$match": {"when": { "$gte": "$from", "$lte": "$to"}, "workflow.state": "$state" } },
                {"$group": {"_id": "$type", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1)])}
            ]
        }
    }
    
    
    
    $collStats (aggregation)
    $project (aggregation)
    $match (aggregation)
    $redact (aggregation)
    $limit (aggregation)
    $skip (aggregation)
    $unwind (aggregation)
    $group (aggregation)
    $sample (aggregation)
    $sort (aggregation)
    $geoNear (aggregation)
    $lookup (aggregation)
    $out (aggregation)
    $indexStats (aggregation)
    $facet (aggregation)
    $bucket (aggregation)
    $bucketAuto (aggregation)
    $sortByCount (aggregation)
    $addFields (aggregation)
    $replaceRoot (aggregation)
    $count (aggregation)
    $graphLookup (aggregation)

### Alle tags (title) counting:
'aggregation': {
            'pipeline': [
                {"$unwind": "$tags"},
                {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1), ("_id", -1)])}
            ]
        }


#### Klubb og fra til:
'source': 'observations',
        'aggregation': {
            'pipeline': [
                {"$unwind": "$type"},
                {"$match": {"club": "$club", "when": { "$gte": "$from", "$lte": "$to" } } },
                {"$group": {"_id": "$type", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1)])}
            ]
        }

"""
