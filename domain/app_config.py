from _base import acl_item_schema

RESOURCE_COLLECTION = 'app_config'
BASE_URL = 'app/config'


_schema = {'environment': {'type': 'string',
                           'required': True,
                           'readonly': False,
                           'unique': True
                           },
           'nlf_org_id': {'type': 'integer'},
           'activities': {'type': 'list'},
           'activity_orgs': {'type': 'dict'},
           'nif_roles': {'type': 'dict'},
           'mapping': {'type': 'dict'},
           'inv_mapping': {'type': 'dict'},
           'luftsport': {'type': 'dict'},
           'fallskjerm': {'type': 'dict'},
           'motorfly': {'type': 'dict'},
           'mikrofly': {'type': 'dict'},
           'seilfly': {'type': 'dict'},
           'ballong': {'type': 'dict'},
           'hps': {'type': 'dict'},
           'modellfly': {'type': 'dict'},
           }

definition = {
    'item_title': 'help',
    'url': BASE_URL,
    'datasource': {
        'source': RESOURCE_COLLECTION,
    },

    'additional_lookup': {
        'url': 'regex("[a-zA-Z]+")',
        'field': 'environment',
    },
    'extra_response_fields': ['environment'],
    'versioning': True,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],

    'mongo_indexes': {'environment': ([('environment', 1)], {'background': True}),
                      # 'acl': ([('acl', 1)], {'background': True}),
                      },

    'schema': _schema

}
