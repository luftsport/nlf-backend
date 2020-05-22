"""
    Custom content
    ==============

"""

from flask import Blueprint, current_app as app, request, Response, abort, jsonify
from ext.scf import ACL_CLOSED_ALL_LIST, ACL_CONTENT_USERS
from eve.methods.get import getitem_internal
from eve.methods.patch import patch_internal
from ext.app.eve_helper import eve_abort, eve_response, eve_error_response
from ext.app.decorators import *

Content = Blueprint('Custom content resource', __name__, )


@Content.route("/publish/<objectid:content_id>", methods=['POST', 'DELETE'])
@require_token()
def publish(content_id):


    lookup = {
        '_id': content_id,
        '$or': [{"acl.execute.roles": {'$in': app.globals['acl']['roles']}},
                {"acl.execute.users": {'$in': [app.globals.get('user_id')]}}]
    }

    acl = {
        'read': {
            'users': [app.globals.get('user_id')],
            'roles': ACL_CLOSED_ALL_LIST if request.method == 'POST' else []
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

    published = True if request.method == 'POST' else False

    # response, last_modified, etag, status
    response, last_modified, etag, status = patch_internal('content',
                                                           {
                                                               'acl': acl,
                                                               'published': published,
                                                               'owner': app.globals.get('user_id')
                                                           },
                                                           False,
                                                           True,
                                                           **lookup)
    print(response, status)
    if status in [200,201]:
        return eve_response(response, status)

    else:
        print(response, status)

    return eve_error_response('Error', 403)

