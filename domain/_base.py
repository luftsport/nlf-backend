"""

    Base schemas
    ============
    
    Reusable schemas for resource definitions

"""

workflow_schema = {
    'type': 'dict',
    'readonly': True,
    'schema': {}
}

watchers_schema = {
    'type': 'list',
    'default': [],
    'readonly': True
}

comments_schema = {
    'type': 'list',
    'default': [],
    'readonly': True,
    'schema': {
        'type': 'dict',
        'schema': {
            'date': {'type': 'datetime'},
            'user': {'type': 'integer'},
            'comment': {'type': 'string'}
        }
    }
}

ask_schema = {
    'type': 'dict',
    'schema': {'attitude': {'type': 'integer'},
               'skills': {'type': 'integer'},
               'knowledge': {'type': 'integer'},
               'text': {'type': 'dict'}
               },
    'default': {'attitude': 0,
                'skills': 0,
                'knowledge': 0,
                'text': {}
                }
}

acl_role_schema = {
    'type': 'dict',
    'schema': {
        'activity': {'type': 'integer'},
        'org': {'type': 'integer'},
        'role': {'type': 'integer'}
    }
}

acl_type_schema = {
    'type': 'dict',
    'schema': {'users': {'type': 'list'},
               'roles': {'type': 'list'}}
}

acl_item_schema = {
    'type': 'dict',
    'readonly': True,
    'schema': {'read': {'type': 'dict', 'schema': acl_type_schema},
               'write': {'type': 'dict', 'schema': acl_type_schema},
               'execute': {'type': 'dict', 'schema': acl_type_schema},
               'delete': {'type': 'dict', 'schema': acl_type_schema},
               }
}

labels_schema = {
    'type': 'list',
    'default': []
}

geo_schema = {
    'geo': {'type': 'point'},
    'geo_class': {'type': 'string'},
    'geo_importance': {'type': 'float'},
    'geo_place_id': {'type': 'integer'},
    'geo_type': {'type': 'string'}
}

location_schema = {
    'type': 'dict',
    'schema': {
        'street': {'type': 'string'},
        'zip': {'type': 'string'},
        'city': {'type': 'string'},
        'country': {'type': 'string'}
    }
}

location_geo_schema = {
    'type': 'dict',
    'schema': {
        'street': {'type': 'string'},
        'zip': {'type': 'string'},
        'city': {'type': 'string'},
        'country': {'type': 'string'},
        'geo': {'type': 'point'},
        'geo_class': {'type': 'string'},
        'geo_importance': {'type': 'float'},
        'geo_place_id': {'type': 'integer'},
        'geo_type': {'type': 'string'}
    }
}
