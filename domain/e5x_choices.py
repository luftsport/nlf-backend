RESOURCE_COLLECTION = 'e5x_choices'
BASE_URL = 'e5x/choices'

_schema = {

    'key': {'type': 'string'},
    'id': {'type': 'integer', 'nullable': True},
    'label': {'type': 'string', 'nullable': True},
    'descr': {'type': 'string', 'nullable': True},
    'expl': {'type': 'string', 'nullable': True},
    'fir': {'type': 'string', 'nullable': True},
    'iata': {'type': 'string', 'nullable': True},
    'icao': {'type': 'string', 'nullable': True},
    'category': {'type': 'string', 'nullable': True},
    'sub_category': {'type': 'string', 'nullable': True},
    'cert_country': {'type': 'string', 'nullable': True},
    'easa_certificate': {'type': 'string', 'nullable': True},
    'icao_type': {'type': 'string', 'nullable': True},
    'tc_holder': {'type': 'string', 'nullable': True},
    'tc_name': {'type': 'string', 'nullable': True},
    'cictt_td': {'type': 'string', 'nullable': True},
    'tch_country': {'type': 'string', 'nullable': True},
    'type_description': {'type': 'string', 'nullable': True},
    'rit_version': {'type': 'string'}
}

definition = {
    'item_title': 'E5X Attribute Choices',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   },
    'additional_lookup': {
        # 'url': 'regex("[a-z.0-9-]+")',
        # 'field': 'key',
        'url': 'regex("[0-9-]+")',
        'field': 'id',
    },
    'extra_response_fields': ['attribute'],
    'versioning': False,
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'mongo_indexes': {'attr': ([('key', 1), ('id', 1)], {'background': True}),
                      'icao': ([('icao', 1)], {'background': True}),
                      'etag': ([('_etag', 1)], {'background': True, 'unique': True}),
                      'content': ([('descr', 'text'), ('label', 'text')], {'background': True}),
                      'rit_version': ([('rit_version', 1)], {'background': True})
                      },
    'allow_unknown': True,
    'schema': _schema

}

from bson import SON, ObjectId

agg_count_keys = {
    'url': 'e5x/choices/keys/count',
    'item_title': 'E5X choices count',
    'pagination': False,
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$group": {"_id": {"key": "$key"}, "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1), ("_id", -1)])}
            ]
        }
    }
}
