"""
    ACL
    ===
    
    Custom wrapper for observation acl's!

"""

from flask import Blueprint, current_app as app, request, Response, abort, jsonify
from bson import json_util
import json

# from eve.methods.patch import patch_internal

from bson.objectid import ObjectId
# Need custom decorators
from ext.app.decorators import *

from ext.auth.acl import get_acl, modify_user_acl
from ext.app.eve_helper import eve_abort, eve_response


ACLObservations = Blueprint('Acl for observations', __name__, )

@ACLObservations.route("/<string:activity>/<objectid:_id>/<string:right>/<int:person_id>", methods=['DELETE', 'POST'])
@require_token()
def acl_toggle(activity, _id, right, person_id ):

    if person_id != app.globals.get('user_id'):
        # projection={'acl': 1}, right='read'
        status, acl, _ = get_acl('{}_observations'.format(activity), _id, projection={'acl': 1, 'reporter': 1}, right='execute')

        if status is True:

            if request.method == 'POST':
                update = modify_user_acl('{}_observations'.format(activity), _id, person_id, right, 'add')

            elif request.method == 'DELETE':
                update = modify_user_acl('{}_observations'.format(activity), _id, person_id, right, 'remove')


            if update is True:
                return eve_response(True, 201)

    return eve_response(False, 409)