"""
    ACL
    ===
    
    Custom wrapper for acl's!
    
    
"""

from flask import g, Blueprint, current_app as app, request, Response, abort, jsonify
from bson import json_util
import json

###
import uuid
import datetime
####


# from eve.methods.patch import patch_internal

from bson.objectid import ObjectId
# Need custom decorators
from ext.app.decorators import *

import ext.auth.acl as acl_helper
from ext.app.eve_helper import eve_abort, eve_response
from ext.app.notifications import ors_acl

ACL = Blueprint('Acl', __name__, )


####### SOME ACL STUFF ##########
@ACL.route("/users/<string:collection>/<objectid:_id>/flat", methods=['GET'])
@require_token()
def get_users_flat(collection, _id):
    status, acl, _ = acl_helper.get_acl(collection, _id)
    if status is True:
        res = acl_helper.parse_acl(acl)
        k = [p for p in list(set(res['read'] + res['write'] + res['execute'] + res['delete'])) if
             p != g.user_id]

        return eve_response(k)

    else:
        return eve_response({})


@ACL.route("/users/<string:collection>/<objectid:_id>", methods=['GET'])
@require_token()
def get_users(collection, _id):
    status, acl, _ = acl_helper.get_acl(collection, _id)
    if status is True:
        res = acl_helper.parse_acl(acl)

        return eve_response(res)

    else:
        return eve_response({})


@ACL.route("/<string:collection>/<int:observation_id>", methods=['GET'])
@require_token()
def get_observation_user_acl(collection, observation_id):
    result = acl_helper.get_user_permissions(observation_id, collection)

    return eve_response(result)


@ACL.route("/observations/<string:activity>/<objectid:_id>/<string:right>/<int:person_id>", methods=['DELETE', 'POST'])
@require_token()
def acl_toggle(activity, _id, right, person_id):
    if person_id != g.user_id:
        # projection={'acl': 1}, right='read'
        status, acl, ors = acl_helper.get_acl('{}_observations'.format(activity), _id,
                                              projection={'acl': 1, 'reporter': 1, 'id': 1, 'discipline': 1, 'tags': 1},
                                              right='execute')

        if status is True:

            if request.method == 'POST':
                verb = 'tildelte'
                update = acl_helper.modify_user_acl('{}_observations'.format(activity), _id, person_id, right, 'add')

            elif request.method == 'DELETE':
                verb = 'fjernet'
                update = acl_helper.modify_user_acl('{}_observations'.format(activity), _id, person_id, right, 'remove')

            if update is True:
                # recepients, event_from, event_from_id, right, verb,
                ors_acl(
                    recepients=person_id,
                    event_from='{}_observations'.format(activity),
                    event_from_id=_id,
                    right=right,
                    verb='remove' if verb == 'fjernet' else 'add',
                    ors_id=ors.get('id', None),
                    org_id=ors.get('discipline', None),
                    ors_tags=ors.get('tags', [])
                )

                return eve_response(True, 201)

    return eve_response(False, 409)