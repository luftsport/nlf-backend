"""
    Custom lungo passthrough route
    ==============================

    Basically a clean passthrough to Lungo

"""
import datetime

from flask import Blueprint, request, current_app as app, g
from ext.scf import LUNGO_HEADERS, LUNGO_URL, LUNGO_ADDRESS
from ext.app.eve_helper import eve_response, eve_abort
from ext.app.decorators import require_token, require_client_access_token
import requests
# from dateutil.relativedelta import relativedelta
# from dateutil import parser
# Supress insecre warning
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Lungo = Blueprint('Lungo passthrough', __name__, )


@Lungo.route("/syncdaemon/workers/start", methods=["POST"])
@require_token()
def syncdaemon_workers_start():
    headers = LUNGO_HEADERS.copy()
    headers['X-On-Behalf-Of'] = g.id
    resp = requests.post('{}/syncdaemon/workers/start'.format(LUNGO_URL),
                         data=None,
                         headers=headers,
                         verify=app.config.get('REQUESTS_VERIFY', True))

    return eve_response(resp.json(), resp.status_code)


@Lungo.route("/syncdaemon/worker/reboot/<int:index>", methods=["POST"])
@require_token()
def lungo_worker_reboot(index):
    headers = LUNGO_HEADERS.copy()
    headers['X-On-Behalf-Of'] = g.id
    resp = requests.post('{}/syncdaemon/worker/reboot/{}'.format(LUNGO_URL, index),
                         data=None,
                         headers=headers,
                         verify=app.config.get('REQUESTS_VERIFY', True))

    return eve_response(resp.json(), resp.status_code)


@Lungo.route("/nif/change/", methods=["POST"])
@require_token()
def lungo_change_message():
    headers = LUNGO_HEADERS.copy()
    headers['X-On-Behalf-Of'] = g.id
    data = request.get_json()
    resp = requests.post('{}/nif/change/'.format(LUNGO_URL),
                         json=data,
                         headers=headers,
                         verify=app.config.get('REQUESTS_VERIFY', True))

    return eve_response(resp.json(), resp.status_code)

@Lungo.route("/", defaults={"path": ""}, methods=['GET'])
@Lungo.route("/persons/search",defaults={"path": "persons/search"}, methods=['GET'])
@Lungo.route("/<string:path>", methods=['GET'])
@Lungo.route("/<path:path>", methods=['GET'])
@require_token()
def lungo(path):
    headers = LUNGO_HEADERS.copy()
    headers['X-On-Behalf-Of'] = str(g.id)
    resp = requests.get('{}/{}'.format(LUNGO_URL, path),
                        params=request.args.to_dict(),
                        headers=headers,
                        verify=app.config.get('REQUESTS_VERIFY', True))

    try:
        return eve_response(resp.json(), resp.status_code)
    except Exception as e:
        app.logger.exception('Error in Lungo response')
        app.logger.error(resp.text)

    return eve_abort(502, 'Unknown error')
"""
    General Lungo passthrough route
    Catches all GET requests and passes them to Lungo with proper headers   
    
    Check roles and how to return data - persons needs to be stripped
    Embedded needs to be removed from functions, competences etc? 
    
    Working on an obsreg - needs to be able to get more information!   
"""
@Lungo.route("/persons", defaults={"path": ""}, methods=['GET'])
@Lungo.route("/persons/", methods=['GET'])
@Lungo.route("/persons/<objectid:_id>", methods=['GET'])
@Lungo.route("/persons/<int:_id>", methods=['GET'])
@require_token()
def persons(_id=''):
    headers = LUNGO_HEADERS.copy()
    headers['X-On-Behalf-Of'] = str(g.id)
    params = request.args.to_dict()
    # if 'where' not in params:
    #    params['where'] = {}
    # if '_merged_to'params['where']

    resp = requests.get(f'{LUNGO_URL}/persons/{_id}',
                        params=params,
                        headers=headers,
                        verify=app.config.get('REQUESTS_VERIFY', True))

    try:
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data.get('_items', None), list):
                for person in data['_items']:
                    # person['age'] = relativedelta(datetime.datetime.utcnow(), parser.parse(data['birth_date']))
                    person.pop('birth_date', None)
                    person.pop('file_upload_id', None)
                    person.pop('sport_no', None)
                    person.pop('user_id', None)
                    person.pop('settings', None)
                    person.pop('nationality_id', None)
                    person.pop('settings', None)
                    person['address'] = {}
                    # person['address'].pop('contact_information_id', None)
                    # person['address'].pop('phone_home', None)
                    # person['address'].pop('phone_mobile', None)
                    # person['address'].pop('contact_id', None)
                    # person['address'].pop('contact_id', None)
                    # person['address'].pop('contact_id', None)

                    for federation in person.get('federation', []):
                        federation.pop('amount', None)
                    for membership in person.get('memberships', []):
                        if 'payment' in membership:
                            membership['payment'].pop('amount', None)

            elif isinstance(data, dict):
                # data['age'] = relativedelta(datetime.datetime.utcnow(), parser.parse(data['birth_date']))
                data.pop('birth_date', None)
                data.pop('file_upload_id', None)
                data.pop('sport_no', None)
                data.pop('user_id', None)
                data.pop('settings', None)
                data.pop('nationality_id', None)
                data.pop('settings', None)
                data['address'] = {}
                for federation in data.get('federation', []):
                    federation.pop('amount', None)
                for membership in data.get('memberships', []):
                    if 'payment' in membership:
                        membership['payment'].pop('amount', None)

            return eve_response(data, resp.status_code)
        return eve_response(resp.json(), resp.status_code)
    except Exception as e:
        app.logger.exception('Error in Lungo response')
        app.logger.error(resp.text)

    return eve_abort(502, 'Unknown error')

@Lungo.route("/persons/avatar/<int:person_id>", methods=['GET'])
@require_client_access_token()
def lungo_reverse_get_avatar(person_id):

    try:
        # Need proxy upstream address
        # if str(request.remote_addr) != LUNGO_ADDRESS:
        #    return eve_response(None, 403)

        app.logger.info('Lungo is asking for avatar for person_id {}'.format(person_id))
        users = app.data.driver.db['users']
        result = users.find_one({'$or': [{'id': person_id}, {'last_person_id': person_id}, {'merged_from': {'$in': [person_id]}}]}, {'avatar': 1, 'last_user_id': 1})
        if result is not None:
            avatar = result.get('avatar', None)
            last_user_id = result.get('last_user_id', person_id)
            return eve_response({'person_id': last_user_id, 'avatar': avatar}, 200)
        else:
            return eve_response({'person_id': person_id, 'avatar': None}, 404)
    except Exception as e:
        app.logger.exception('Error fetching avatar for person_id {}'.format(person_id))

    return eve_response({'person_id': person_id, 'avatar': None}, 500)

