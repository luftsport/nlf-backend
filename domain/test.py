from bson import SON
from datetime import datetime

RESOURCE_COLLECTION = 'f_observations'
BASE_URL = 'f/observations'

definition = {
    'item_title': 'Observation Aggregations',
    'url': '{}/aggregate'.format(BASE_URL),
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
}

"""
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