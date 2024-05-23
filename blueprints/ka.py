from nif_tools import KA
from flask import Blueprint, current_app as app, request, Response, abort, jsonify
from eve.methods.post import post_internal
import datetime
import hashlib
from ext.auth.decorators import require_token
from ext.auth.clients import users

KA = Blueprint('KA functionality', __name__)

def _gen_change_msg(entity_id, entity_type, change_type, org_id=376, realm='PROD'):
    payload = {}
    sequence_ordinal = datetime.datetime.utcnow()

    payload['id'] = entity_id

    payload['change_type'] = change_type
    payload['entity_type'] = entity_type
    payload['created'] = sequence_ordinal
    payload['modified'] = sequence_ordinal
    payload['merge_result_of'] = []
    payload['name'] = 'Manuell endringsmelding'
    payload['_ordinal'] = hashlib.sha224(bytearray("%s%s%s%s" % (entity_type,
                                                                 entity_id,
                                                                 sequence_ordinal,
                                                                 org_id),
                                                   'utf-8')).hexdigest()
    payload['_status'] = 'ready'
    payload['_org_id'] = org_id
    payload['_realm'] = realm

    resp, _, _, status_code, location_header = post_internal('integration_changes', payl=payload)
    if status_code in [200, 201]:
        return True, resp

    return False, resp

@KA.route('/gcm', methods=['POST'])
@require_token()
def generate_change_message():


    return eve_abort(403)