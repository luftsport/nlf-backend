from flask import g, current_app as app
from ext.app.eve_helper import eve_abort
from ext.scf import ACL_CONTENT_USERS


def before_insert(items):
    if g.user_id not in ACL_CONTENT_USERS:
        return eve_abort(403, 'No access')
        raise Exception

    for document in items:
        document['owner'] = g.user_id


def pre_PATCH(request, lookup):
    lookup.update({'$or': [{"acl.write.roles": {'$in': g.acl.get('roles', [])}},
                           {"acl.write.users": {'$in': [g.user_id]}}]})


def on_before_replace(item, original):
    item['owner'] = g.user_id


def on_before_update(item, original):
    item['owner'] = g.user_id


def pre_DELETE(request, lookup):
    lookup.update({'$or': [{"acl.delete.roles": {'$in': g.acl.get('roles', [])}},
                           {"acl.delete.users": {'$in': [g.user_id]}}]})


def pre_GET(request, lookup):
    lookup.update({'$or': [{"acl.read.roles": {'$in': g.acl.get('roles', [])}},
                           {"acl.read.users": {'$in': [g.user_id]}}]})
