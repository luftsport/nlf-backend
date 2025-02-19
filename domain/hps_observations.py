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
# from hps_observation_components import components_schema
from datetime import datetime
from bson import SON

RESOURCE_COLLECTION = 'hps_observations'
BASE_URL = 'hps/observations'

ORS_MODEL_TYPE = 'hps'
ORS_MODEL_VERSION = 1

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
    'item_title': 'Hps Observations',
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

        # Forløpet
        'components.attributes',
        'components.flags',
        'components.where.at',
        'components.where.altitude',
        'components.what',
        # Involverte
        'involved.data.activity',
        'involved.data.years_of_experience',
        'involved.data.altitude',
        'involved.data.aircraft',
        'involved.data.age',
        'involved.data.competences._code',
        'involved.data.competences.type_id',
        'involved.data.gear.harness',
        'involved.data.gear.harness_experience',
        'involved.data.gear.main_canopy',
        'involved.data.gear.main_canopy_experience',
        'involved.data.gear.main_canopy_size',
        'involved.data.gear.reserve_canopy',
        'involved.data.gear.reserve_canopy_size',
        'involved.data.gear.aad',
        'involved.data.gear.other',
        'involved.fu',
        'involved.ph',

        # Ratings
        'rating.potential',
        'rating.actual',
        'rating._rating',

        # Flags
        'flag.insurance',
        'flag.aviation',

        # WX
        'weather.manual.clouds.base',
        'weather.manual.clouds.fog',
        'weather.manual.clouds.hail',
        'weather.manual.clouds.rain',
        'weather.manual.clouds.snow',
        'weather.manual.clouds.thunder',
        'weather.manual.temp.altitude',
        'weather.manual.temp.ground',
        'weather.manual.wind.avg',
        'weather.manual.wind.dir',
        'weather.manual.wind.max',
        'weather.manual.wind.min',
        'weather.manual.wind.turbulence',
        'weather.manual.wind.gusting',

        # Workflow
        'workflow.state',
        # Flags
        'flags',
        # Rating
        'rating',
        # Location
        'location',
        # Været,
        'weather',
        # Tiltak
        'actions.local',
        'actions.central',
        # Root
        'id',
        '_id',
        'when',
        'club',
        'discipline',
        'tags',
        'type',
        '_updated',
        '_created'
    ],
    'versioning': True,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'PUT'],
    'mongo_indexes': {
        'id': ([('id', 1)], {'background': True}),
        'club': ([('club', 1)], {'background': True}),
        'discipline': ([('discipline', 1)], {'background': True}),
        'persons': ([('owner', 1), ('reporter', 1)], {'background': True}),
        'when': ([('when', 1)], {'background': True}),
        'type': ([('type', 1)], {'background': True}),
        'rating': ([('rating', 1)], {'background': True}),
        'title': (
            [('title', 'text'), ('tags', 'text'), ('ask', 'text'), ('ask', 'text'), ('components.what', 'text'), ('components.how', 'text')],
            {'background': True,
             'default_language': 'norwegian',
             'weights': {'title': 10, 'tags': 5, 'ask': 2}}
        )
    },
    'schema': _schema

}

# Hook setting only execute
workflow_todo = {
    'item_title': 'Hps Observations Todo',
    'url': '{}/workflow/todo'.format(BASE_URL),
    'datasource': {'source': RESOURCE_COLLECTION,
                   'projection': {'acl': 1, 'id': 1, 'when': 1, 'tags': 1, 'workflow': 1, 'type': 1, '_model': 1}
                   # 'files': 0,
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
    'item_title': 'Hps Observations Self',
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
                {"$match": {"workflow.state": "closed", "when": {"$gte": "$from", "$lte": "$to"},
                            "discipline": "$discipline"}},
                {"$group": {"_id": "$discipline", "avg": {"$avg": "$rating._rating"}, "sum": {"$sum": 1}}},
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

# Medlemmer i en klubb med rapporter i andre klubber
aggregate_user_other_discipline = {
    'item_title': 'Observations aggregate own members reported in other clubs',
    'url': '{}/aggregate/users/foreign'.format(BASE_URL),
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {'$match':
                    {
                        '$and': [
                            {'involved.data.memberships.discipline': '$discipline'},
                            {'discipline': {'$ne': '$discipline'}}
                        ]
                    }
                },
                {
                    '$unwind': {
                        'path': '$involved',
                    },
                },
                {
                    '$match': {
                        'involved.data.memberships.discipline': '$discipline',
                    },
                },
                {
                    '$project': {
                        'id': 1,
                        'tags': 1,
                        'title': 1,
                        'club': 1,
                        'discipline': 1,
                        'when': 1,
                        'location': 1,
                        'involved.id': 1,
                        'rating': 1,
                        '_id': 0,
                    },
                },
            ]
        }
    }
}

# Rapporter der observatøren selv har rapportert
aggregate_users_count_created_reports = {
    'item_title': 'Observations aggregate count number of created reports per user',
    'url': '{}/aggregate/users/reports/created/count'.format(BASE_URL),
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$match": {"discipline": "$discipline"}},  # {"discipline": "$discipline"}},
                {
                    "$group": {
                        "_id": "$reporter",
                        "total": {"$sum": 1}
                    },
                },
                {'$sort': {
                    'total': -1
                }}
            ]
        }
    }
}

# Antall rapporter som involvert
aggregate_users_count = {
    'item_title': 'Observations aggregate count number of reports per involved',
    'url': '{}/aggregate/users/reports/count'.format(BASE_URL),
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$match": {"involved.data.memberships.discipline": "$discipline"}},
                # {"discipline": "$discipline"}},
                {"$unwind": "$involved"},
                {
                    "$group": {
                        "_id": "$involved.id",
                        "total": {"$sum": 1}
                    },
                },
                {'$sort': {
                    'total': -1
                }}]
        }
    }
}
# Returnerer alle observasjoner på en bruker
aggregate_user_reports = {
    'item_title': 'Observations (aggregate) get reports as involved',
    'url': '{}/aggregate/user/reports'.format(BASE_URL),
    'datasource': {
        'source': RESOURCE_COLLECTION,
        'aggregation': {
            'pipeline': [
                {"$match": {"involved.id": "$person_id"}},
                {
                    '$project': {
                        'id': 1,
                        'tags': 1,
                        'title': 1,
                        'type': 1,
                        'club': 1,
                        'discipline': 1,
                        'when': 1,
                        'location': 1,
                        'involved.id': 1,
                        'reporter': 1,
                        '_id': 0,
                        'rating': 1
                    },
                },
                {"$sort": {"when": -1}}
            ]
        }
    }
}
