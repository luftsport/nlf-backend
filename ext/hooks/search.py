from flask import g, current_app as app
from ext.app.eve_helper import eve_abort
import json
from bson.objectid import ObjectId

from eve.methods.get import getitem_internal
from ext.auth.acl import has_permission
from ext.app.decorators import *


@require_token()
def before_get(request, lookup):
    lookup.update({'$or': [{"acl.read.roles": {'$in': g.acl.get('roles', [])}},
                           {"acl.read.users": {'$in': [g.user_id]}}]})


@require_token()
def before_patch(request, lookup):
    lookup.update({'$or': [{"acl.write.roles": {'$in': g.acl.get('roles', [])}},
                           {"acl.write.users": {'$in': [g.user_id]}}]})

@require_token()
def before_remove(request, lookup):
    lookup.update({'$or': [{"acl.execute.roles": {'$in': g.acl.get('roles', [])}},
                           {"acl.execute.users": {'$in': [g.user_id]}}]})

@require_token()
def before_insert(items):
    for item in items:
        before_insert_item(item)

@require_token()
def before_insert_item(item):
    try:

        item['owner'] = g.user_id
        # Set acl!
        item['acl'] = {
            'read': {
                'users': [g.user_id],
                'roles': []
            },
            'execute': {
                'users': [g.user_id],
                'roles': []
            },
            'write': {
                'users': [g.user_id],
                'roles': []
            },
            'delete': {
                'users': [],
                'roles': []
            }
        }

    except Exception as e:
        return eve_abort(422, 'Could not create search')
