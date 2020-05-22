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
# from f_observation_components import components_schema
from datetime import datetime
from bson import SON

RESOURCE_COLLECTION = 'motorfly_observations'
BASE_URL = 'motorfly/observations'

ORS_MODEL_TYPE = 'motorfly'
ORS_MODEL_VERSION = 2

_schema = {'id': {'type': 'integer',
                  'readonly': True
                  },
           'e5x': {'type': 'dict'},

           'type': {'type': 'string',
                    'allowed': ['sharing', 'unwanted_act', 'unsafe_act', 'near_miss', 'incident', 'accident'],
                    'default': 'near_miss'
                    },

           'flags': {'type': 'dict',
                     # 'schema': {'school': {'type': 'boolean'},
                     #          'flight_service': {'type': 'boolean'},
                     #          'e5x': {'type': 'boolean'}
                     #          },
                     # 'default': {'school': False,
                     #            'flight_service': False,
                     #            'e5x': False}
                     'default': {}
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
           # E5X
           'aircrafts': {'type': 'list', 'default': []},
           'occurrence': {'type': 'dict', 'default': {}},

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
                      'default': {'type': ORS_MODEL_TYPE, 'version': ORS_MODEL_VERSION}
                      }

           }
# 'schema': components_schema
definition = {
    'item_title': 'Motorfly Observations',
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

workflow_todo = {
    'item_title': 'Motorfly Observations todo',
    'url': '{}/workflow/todo'.format(BASE_URL),
    'datasource': {'source': RESOURCE_COLLECTION,
                   },
    # Make a counter so we can have a lookup for #455
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

aggregate_observation_types = {
    'item_title': 'Observation Aggregations',
    'url': '{}/aggregate'.format(BASE_URL),
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
