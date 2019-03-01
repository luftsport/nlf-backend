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

RESOURCE_COLLECTION = 'motorfly_observations'
BASE_URL = 'motorfly/observations'

_schema = {'id': {'type': 'integer',
                  'required': False,
                  'readonly': True
                  },

           'type': {'type': 'string',
                    'allowed': ['sharing', 'unsafe_act', 'near_miss', 'incident', 'accident']
                    },

           'flags': {'type': 'dict',
                     'schema': {'aviation': {'type': 'boolean', 'default': False},
                                'insurance': {'type': 'boolean', 'default': False}
                                }
                     },
           'ask': ask_schema,

           'tags': {'type': 'list',
                    'default': []
                    },

           'club': {'type': 'integer',
                    'required': True
                    },

           'location': {'type': 'dict',
                        'default': {}},
           'route': {'type': 'dict',
                     'default': {}},
           'flight_log': {'type': 'dict',
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
                      'schema': {'actual': {'type': 'integer', 'default': 1},
                                 'potential': {'type': 'integer', 'default': 1}
                                 }
                      },
           'weather': {'type': 'dict',
                       'schema': {'auto': {'type': 'dict'},
                                  'manual': {'type': 'dict'}
                                  }
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
           'media': {'type': 'list',
                     'schema': {'type': 'string'}
                     },
           'actions': {'type': 'dict'},
           'comments': comments_schema,
           'workflow': workflow_schema,
           'watchers': watchers_schema,
           'acl': acl_item_schema,
           '_model': {'type': 'dict',
                      'schema': {'version': {'type': 'integer', 'default': 1},
                                 'type': {'type': 'string', 'default': 'motorfly'}
                                 }
                      }

           }
# 'schema': components_schema
definition = {
    'item_title': 'Motor Observations',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   'projection': {'acl': 0}  # 'files': 0,
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
                      'persons': ([('owner', 1), ('reporter', 1)], {'background': True}),
                      'when': ([('when', 1)], {'background': True}),
                      'type': ([('type', 1)], {'background': True}),
                      'rating': ([('rating', 1)], {'background': True}),
                      'title': ([('tags', 'text')], {'background': True})

                      },
    'schema': _schema

}
