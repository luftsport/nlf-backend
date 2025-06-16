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

RESOURCE_COLLECTION = 'search'
BASE_URL = 'search'

_schema = {
    'title': {'type': 'string'},
    'rules': {'type': 'dict'},  # where sort page
    'text': {'type': 'string'},
    'options': {'type': 'dict'},
    'collection': {'type': 'string'},
    'notifications': {'type': 'boolean'},
    'meta': {'type': 'dict'},
    'owner': {'type': 'integer'},
    'acl': acl_item_schema,

}
# 'schema': components_schema
definition = {
    'item_title': 'Lagrede søk',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   # 'projection': {'acl': 0}  # 'files': 0,
                   },
    # 'extra_response_fields': ['id'],
    # makes only user access those...
    # 'auth_field': 'owner',
    'allowed_filters': [
        'title',
        'query',
        'collection',
        '_updated',
        '_created'
    ],
    'versioning': True,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'mongo_indexes': {
        'activity': ([('activity', 1)], {'background': True}),
        'title': (
            [('title', 'text')],
            {
                'background': True,
                'default_language': 'norwegian',
                'weights': {'title': 10}
            }
        )

    },
    'schema': _schema

}
