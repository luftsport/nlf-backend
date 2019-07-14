RESOURCE_COLLECTION = 'notifications'
BASE_URL = 'notifications'

_schema = {'type': {'type': 'string',
                    'required': True,
                    },

           'data': {'type': 'dict'},  # what, when, where, who, how
           'dimissable': {'type': 'boolean'},
           'dismissed': {'type': 'datetime'},
           'recepients': {'type': 'list',
                          'schema': {
                              'type': 'integer'
                          }
                          },
           'transports': {'type': 'list'}  # ['email', 'sms', socket',...]
           }

definition = {
    'item_title': 'content',
    'url': BASE_URL,
    'datasource': {'source': RESOURCE_COLLECTION,
                   },
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'mongo_indexes': {
        'housekeeping': ([('type', 1), ('dismissable', 1), ('dismissed', 1), ('transports', 1)], {'background': True}),
        'recepients': ([('recepients', 1)], {'background': True}),
        },
    'schema': _schema

}
