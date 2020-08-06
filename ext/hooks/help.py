from flask import current_app as app
from ext.app.eve_helper import eve_abort
from ext.scf import ACL_HELP_USERS, ACL_CLOSED_ALL_LIST


def before_insert(items):
    if app.globals.get('user_id') not in ACL_HELP_USERS:
        eve_abort(403, 'No access')
        raise Exception

    for document in items:
        document['owner'] = app.globals.get('user_id')

        document['acl'] = {
            'read': {
                'users': [app.globals.get('user_id')],
                'roles': ACL_CLOSED_ALL_LIST
            },
            'write': {
                'users': [app.globals.get('user_id')],
                'roles': []
            },
            'execute': {
                'users': [app.globals.get('user_id')],
                'roles': []
            },
            'delete': {
                'users': [app.globals.get('user_id')],
                'roles': []
            }
        }


def on_before_replace(item, original):
    item['owner'] = app.globals.get('user_id')


def on_before_update(item, original):
    item['owner'] = app.globals.get('user_id')


def pre_PATCH(request, lookup):
    lookup.update({'$or': [{"acl.write.roles": {'$in': app.globals['acl']['roles']}},
                           {"acl.write.users": {'$in': [app.globals.get('user_id')]}}]})


def pre_DELETE(request, lookup):
    lookup.update({'$or': [{"acl.delete.roles": {'$in': app.globals['acl']['roles']}},
                           {"acl.delete.users": {'$in': [app.globals.get('user_id')]}}]})


def pre_GET(request, lookup):
    lookup.update({'$or': [{"acl.read.roles": {'$in': app.globals['acl']['roles']}},
                           {"acl.read.users": {'$in': [app.globals.get('user_id')]}}]})
