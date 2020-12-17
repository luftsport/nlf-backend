"""

    Observations
    ============
    
    @note: workflow kan feks være readonly, så kan dette rutes via en egen (flask) ressurs for å sette den!

    @todo: Observations need an initializing pre_insert/POST to init workflows! 
           Or rather a after with partc_internal since it's a readonly field
    @todo: Add autogenerating id for observation in pre hook
    @todo: Add workflow by default in pre hook
    @todo: add schema for organisation or club + location
"""
from _base import workflow_schema, comments_schema, watchers_schema, acl_item_schema, ask_schema
# from fallskjerm_observation_components import components_schema
from datetime import datetime
from bson import SON

RESOURCE_COLLECTION = 'fallskjerm_observations'
BASE_URL = 'fallskjerm/observations'

ORS_MODEL_TYPE = 'fallskjerm'
ORS_MODEL_VERSION = 3

_schema = {'id': {'type': 'integer',
                  'readonly': True
                  },

           'type': {'type': 'string',
                    'allowed': ['sharing', 'unwanted_act', 'unsafe_act', 'near_miss', 'incident', 'accident'],
                    'default': 'near_miss'
                    },

           'flags': {'type': 'dict',
                     'schema': {'aviation': {'type': 'boolean'},
                                'insurance': {'type': 'boolean'}
                                },
                     'default': {'aviation': False,
                                 'insurance': False}
                     },
           'ask': ask_schema,

           'tags': {'type': 'list',
                    'default': []
                    },

           'club': {'type': 'integer',
                    'required': True
                    },
           'discipline': {'type': 'integer',
                          'required': True
                          },
           'location': {'type': 'dict',
                        'default': {}},

           'owner': {'type': 'integer', 'readonly': True},
           'reporter': {'type': 'integer', 'readonly': True},

           'when': {'type': 'datetime', 'default': datetime.utcnow()},

           'involved': {'type': 'list',
                        'default': []
                        },

           'organization': {'type': 'dict',
                            'default': {}
                            },

           'rating': {'type': 'dict',
                      'schema': {'actual': {'type': 'integer'},
                                 'potential': {'type': 'integer'},
                                 '_rating': {'type': 'integer', 'default': 1}
                                 },
                      'default': {'actual': 1, 'potential': 1}
                      },
           'weather': {'type': 'dict',
                       'schema': {'auto': {'type': 'dict'},
                                  'manual': {'type': 'dict'}
                                  },
                       'default': {'auto': {}, 'manual': {}}
                       },

           'components': {'type': 'list',
                          'default': []

                          },

           'files': {'type': 'list',
                     'schema': {'type': 'dict',
                                'schema': {'f': {'type': 'string'},
                                           'r': {'type': 'boolean'}
                                           }
                                },
                     'default': []
                     },
           'categories': {'type': 'list',
                          'default': []
                          },
           'related': {'type': 'list',
                       'default': []
                       },
           'actions': {'type': 'dict'},
           'comments': comments_schema,
           'workflow': workflow_schema,
           'watchers': watchers_schema,
           'acl': acl_item_schema,
           '_model': {'type': 'dict',
                      'schema': {'version': {'type': 'integer'},
                                 'type': {'type': 'string'}
                                 },
                      'default': {'type': ORS_MODEL_TYPE, 'version': ORS_MODEL_VERSION},
                      'readonly': True
                      }

           }
# 'schema': components_schema
definition = {
    'item_title': 'Fallskjerm Observations',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0}  # 'files': 0,
                   },
    # Make a counter so we can have a lookup for #455
    'additional_lookup': {
        'url': 'regex("[\d{1,9}]+")',
        'field': 'id',
    },
    'extra_response_fields': ['id'],
    # makes only user access those...
    # 'auth_field': 'owner',
    'allowed_filters': [
        'workflow.state',
        'id',
        '_id',
        'when',
        'club',
        'discipline',
        'tags',
        'flags',
        'rating',
        'type',
        'location',
        '_updated',
        '_created'
    ],
    'versioning': True,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'PUT'],
    'mongo_indexes': {'id': ([('id', 1)], {'background': True}),
                      'club': ([('club', 1)], {'background': True}),
                      'discipline': ([('discipline', 1)], {'background': True}),
                      'persons': ([('owner', 1), ('reporter', 1)], {'background': True}),
                      'when': ([('when', 1)], {'background': True}),
                      'type': ([('type', 1)], {'background': True}),
                      'rating': ([('rating', 1)], {'background': True}),
                      'title': ([('tags', 'text'), ('ask', 'text')],
                                {'background': True, 'default_language': 'norwegian',
                                 'weights': {'tags': 10, 'ask': 2}})

                      },
    'schema': _schema

}

# Hook setting only exececute
workflow_todo = {
    'item_title': 'Fallskjerm Observations Todo',
    'url': '{}/workflow/todo'.format(BASE_URL),
    'datasource': {'source': RESOURCE_COLLECTION,
                   'projection': {'acl': 1, 'id': 1, 'when': 1, 'tags': 1, 'workflow': 1, 'type': 1, '_model': 1}  # 'files': 0,
                   },
    'additional_lookup': {
        'url': 'regex("[\d{1,9}]+")',
        'field': 'id',
    },
    'extra_response_fields': ['id'],
    'allowed_filters': [],
    'versioning': False,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'schema': _schema
}

# My own, hook sets lookup to user
user = {
    'item_title': 'Fallskjerm Observations Self',
    'url': '{}/user'.format(BASE_URL),
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 1, 'id': 1, 'when': 1, 'tags': 1, 'workflow': 1, 'type': 1}  # 'files': 0,
                   },
    'additional_lookup': {
        'url': 'regex("[\d{1,9}]+")',
        'field': 'id',
    },
    'extra_response_fields': ['id'],
    'versioning': False,
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'schema': _schema
}

aggregate_types = {
    'item_title': 'Observation Aggregations by types',
    'url': '{}/aggregate/types'.format(BASE_URL),
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$unwind": "$type"},
                {"$match": {"when": {"$gte": "$from", "$lte": "$to"}, "workflow.state": "$state"}},
                {"$group": {"_id": "$type", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1)])}
            ]
        }
    }
}

aggregate_types_discipline = {
    'item_title': 'Observation Aggregations by discipline and types',
    'url': '{}/aggregate/types/discipline'.format(BASE_URL),
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$unwind": "$type"},
                {"$match": {"when": {"$gte": "$from", "$lte": "$to"}, "discipline": "$discipline",
                            "workflow.state": "$state"}},
                {"$group": {"_id": "$type", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1)])}
            ]
        }
    }
}

aggregate_states_discipline = {
    'item_title': 'Observation Aggregation by discipline and states',
    'url': '{}/aggregate/states/discipline'.format(BASE_URL),
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$unwind": "$workflow.state"},
                {"$match": {"when": {"$gte": "$from", "$lte": "$to"}, "discipline": "$discipline"}},
                {"$group": {"_id": "$workflow.state", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1)])}
            ]
        }
    }
}

aggregate_avg_rating_discipline = {
    'item_title': 'Observations aggregate average ratings by discipline and date range',
    'url': '{}/aggregate/ratings/discipline'.format(BASE_URL),
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$match": {"workflow.state": "closed", "when": {"$gte": "$from", "$lte": "$to"}, "discipline": "$discipline"}},
                {"$group": {"_id": "$discipline", "avg": {"$avg": "$rating._rating"}}},
            ]
        }
    }
}

aggregate_avg_rating = {
    'item_title': 'Observations aggregate average ratings by discipline and date range',
    'url': '{}/aggregate/ratings'.format(BASE_URL),
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$match": {"when": {"$gte": "$from", "$lte": "$to"}, "workflow.state": "closed"}},
                {"$group": {"_id": "$discipline", "avg": {"$avg": "$rating._rating"}}},
                {"$sort": SON([("avg", -1)])}
            ]
        }
    }
}


