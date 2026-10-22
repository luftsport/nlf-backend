"""
    Custom lungo passthrough route
    ==============================

    Basically a clean passthrough to Lungo

"""
import datetime

from flask import Blueprint, request, current_app as app, g, abort
from ext.scf import LUNGO_HEADERS, LUNGO_URL, LUNGO_ADDRESS
from ext.app.eve_helper import eve_response, eve_abort
from ext.app.decorators import require_token, require_client_access_token
from ext.auth.anonymizer import anonymize_ors
from ext.app.eve_blueprint_helper import parse_request, parsed_to_pymongo, get_data_driver, execute_parsed_query
import requests
# from dateutil.relativedelta import relativedelta
# from dateutil import parser
# Supress insecre warning
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Lungo = Blueprint('Lungo passthrough', __name__, )

## E5X helper functions

from typing import Any, Dict, Union, List, Optional

RIT_VERSION = "4.1.0.3"
class E5XDirectDbResolver:
    """Resolves E5X taxonomy attributes and choice values using native PyMongo."""

    def __init__(self):
        self.db = app.data.driver.db
        self.attr_col = self.db['e5x_attributes']
        self.choice_col = self.db['e5x_choices']

    def get_attribute_by_path(self, path: str) -> Optional[Dict[str, Any]]:
        try:
            return self.attr_col.find_one({"attribute": path, "rit_version": RIT_VERSION})
        except Exception:
            return None

    def get_choice_value(self, choices_key: str, value_id: Union[int, str]) -> Optional[str]:
        try:
            choice = self.choice_col.find_one({"key": choices_key, "id": value_id, "rit_version": RIT_VERSION})
            return choice.get('label') or choice.get('value') if choice else None
        except Exception:
            return None

    def resolve_item(self, path: str, raw_value: Any) -> Dict[str, Any]:
        attribute_meta = self.get_attribute_by_path(path)
        # Fallback if attribute definition is missing in database
        if not attribute_meta:
            # Standardize fallback value to list format
            fallback_list = raw_value if isinstance(raw_value, list) else [raw_value]
            return {
                "label": path,
                "values": [str(v) for v in fallback_list if v is not None]
            }

        display_label = attribute_meta.get('choices_key') or attribute_meta.get('attribute', path)
        choices_key = attribute_meta.get('choices_key')
        # Standardize the incoming values into a working list format
        if isinstance(raw_value, list):
            working_values = raw_value
        elif raw_value is not None:
            working_values = [raw_value]
        else:
            working_values = []

        # Resolve choices if a taxonomy list key exists
        resolved_list = []
        if choices_key:
            for val in working_values:
                translated = self.get_choice_value(choices_key, val)
                resolved_list.append(translated if translated is not None else str(val))
        else:
            resolved_list = [str(val) for val in working_values]

        return {
            "label": display_label,
            "values": resolved_list
        }


def resolve_e5x_payload(path, payload):
    """
    [
        {"path": "E5X.Occurrence", "key": "OccurrenceClass", "value": 3},
        {"path": "E5X.Occurrence.RiskLevel", "value":}
        {"path": "E5X.Occurrence.ContributingFactors", "value": [102, 105]}
    ]
    """
    resolver = E5XDirectDbResolver()
    path = '.'.join(word[0].capitalize()+word[1:] for word in path.split('.'))

    for key, item in payload.items():
        try:
            raw_value = item.get('value')
        except AttributeError as e:
            raw_value = item
        _path = f'{path}.{key[0].capitalize()+key[1:]}'
        _path = _path.replace('Atm', 'ATM').replace('Ecr', 'ERCS')
        resolved = resolver.resolve_item(f'{path}.{key[0].capitalize()+key[1:]}', raw_value)

        payload[key] = {
            "path": path,
            "label": resolved["label"],
            "values": resolved["values"],
            "original_value": raw_value
        }

    return payload

def resolve_e5x_payload_list(path, values):
    for key, value in values:
        resolved = resolver.resolve_item(f"{path}.{key}", value)
        response_data.append({
            "path": f"{path}.{key}",
            "label": resolved["label"],
            "values": resolved["values"]
        })
def clean_e5x_object(obj):
    try:
        # Check if the input is a dictionary
        if isinstance(obj, dict):
            # Iterate over a copy of keys to safely delete items during iteration
            for key in list(obj.keys()):
                value = obj[key]

                # Check for "object" equivalent (dict)
                if isinstance(value, dict):
                    if 'unit' in value:
                        # Corresponds to !value['value'] (checks for falsy values like None, '', 0, False)
                        if ('value' in value and (not value['value'] or value['value'] == '')) or 'value' not in value:
                            del obj[key]
                    elif 'plainText' in value:
                        if not value['plainText'] or value['plainText'] == '':
                            del obj[key]
                    else:
                        # Recurse...
                        clean_e5x_object(value)

                    # ...and remove if now "empty" (checks if dictionary has no keys left)
                    # This must run only if the key wasn't already deleted above
                    if key in obj and isinstance(obj[key], dict) and not obj[key]:
                        del obj[key]

                # Check for None (closest Python equivalent to JS "undefined" in APIs/JSON)
                elif value is None:
                    del obj[key]

                # Check for lists (arrays) that are empty
                elif isinstance(value, list) and len(value) == 0:
                    del obj[key]

    except Exception:
        pass

    return obj


def e5x_parse_label(path: str) -> str:
    try:
        last_part = path.split('.')[-1] if path else ''

        # Split by uppercase letters (lookahead)
        tmp = [s for s in re.split(r'(?=[A-Z])', last_part) if s]
        label = ''

        for idx, item in enumerate(tmp):
            # Check if current and previous elements are single uppercase letters
            if (
                    len(item) == 1 and item.isupper() and
                    idx > 0 and len(tmp[idx - 1]) == 1 and tmp[idx - 1].isupper()
            ):
                label += item
            else:
                label += ' ' + item

        # Trim spaces and capitalize the very first letter
        return label.strip().capitalize()
    except Exception:
        return ''

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
@Lungo.route("/persons/search", defaults={"path": "persons/search"}, methods=['GET'])
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
def reverse_get_avatar(person_id):
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


@Lungo.route("/obsreg/<string:activity>", methods=['GET'])
@require_client_access_token()
def reverse_get_obsregs(activity):
    driver = app.data.driver
    col = driver.db[f'{activity}_observations']
    try:
        if activity not in ['fallskjerm', 'motorfly', 'sportsfly', 'seilfly']:
            return abort(404, description="Activity not found or allowed")

        parsed = parse_request(resource=f'{activity}_observations', is_blueprint=False, trigger_hooks=False)
        results = list(execute_parsed_query(collection=get_data_driver(f'{activity}_observations'), parsed=parsed))

        r = []
        for idx, item in enumerate(results):
            r.append(anonymize_ors(item))

        return eve_response(r, 200)

    except Exception as e:
        app.logger.exception('Error fetching obsregs for activity {}'.format(activity))

    return eve_response({'activity': activity, 'obsreg': None}, 500)

def fix_camelcase(s):
    if 'atm' or 'Atm' in s:
        return s.replace('atm', 'ATM').replace('Atm', 'ATM')
    if 'ecr' or 'Ecr' in s:
        return s.replace('ecr', 'ERCS').replace('Ecr', 'ERCS')

    return s

@Lungo.route("/obsreg/<string:activity>/<int:obsreg_id>", methods=['GET'])
@require_client_access_token()
def reverse_get_obsreg(activity, obsreg_id):
    try:
        driver = app.data.driver
        col = driver.db[f'{activity}_observations']
        if activity not in ['fallskjerm', 'motorfly', 'sportsfly', 'seilfly']:
            return abort(404, description="Activity not found or allowed")
        app.logger.info('Lungo is asking for obsreg for activity {} and obsreg_id {}'.format(activity, obsreg_id))
        obsregs = app.data.driver.db[f'{activity}_observations']
        result = obsregs.find_one({'id': obsreg_id})

        if result is not None:
            if 'occurrence' in result:
                result['occurrence']['attributes'] = clean_e5x_object(result['occurrence']['attributes'])
                result['occurrence']['entities'] = clean_e5x_object(result['occurrence']['entities'])

                result['occurrence']['attributes'] = resolve_e5x_payload('E5X.Occurrence', result['occurrence']['attributes'])

                for key, entity in result['occurrence']['entities'].items():
                    if isinstance(result['occurrence']['entities'][key], list):
                        for idx, entity in enumerate(result['occurrence']['entities'][key]):

                            result['occurrence']['entities'][key][idx]['attributes'] = resolve_e5x_payload(f'E5X.Occurrence.{fix_camelcase(key)}', entity['attributes'])
                    else:
                        result['occurrence']['entities'][key]['attributes'] = resolve_e5x_payload(f'E5X.Occurrence.{fix_camelcase(key)}', result['occurrence']['entities'][key]['attributes'])
            if 'aircrafts' in result:
                for idx, aircraft in enumerate(result['aircrafts']):
                    result['aircrafts'][idx]['aircraft']['e5x'] = aircraft = clean_e5x_object(result['aircrafts'][idx]['aircraft']['e5x'])
                    # Attributes
                    for key, item in result['aircrafts'][idx]['aircraft']['e5x'].get('attributes', {}).items():
                        result['aircrafts'][idx]['aircraft']['e5x']['attributes'][key] = resolve_e5x_payload(f'E5X.Occurrence.Aircraft', {key: item})
                    # Entities
                    for key, item in result['aircrafts'][idx]['aircraft']['e5x'].get('entities', {}).items():
                        if isinstance(eitem, list):
                            for eidx, entity in enumerate(eitem):
                                result['aircrafts'][idx]['aircraft']['e5x']['entities'][key][eidx]['attributes'] = resolve_e5x_payload(f'E5X.Occurrence.Aircraft', entity['attributes'])
                        else:
                            result['aircrafts'][idx]['aircraft']['e5x']['entities'][key]['attributes'] = resolve_e5x_payload(f'E5X.Occurrence.Aircraft', item['attributes'])

                if 'airspace' in result['aircrafts'][idx]:
                    result['aircrafts'][idx]['airspace'] = clean_e5x_object(result['aircrafts'][idx]['airspace'])
                    # Attributes
                    for key, item in result['aircrafts'][idx]['airspace'].get('attributes', {}).items():
                        result['aircrafts'][idx]['airspace']['attributes'][key] = resolve_e5x_payload(f'E5X.Occurrence.AirSpace', {key: item})
                    # Entities
                    for key, item in result['aircrafts'][idx]['airspace'].get('entities', {}).items():
                        if isinstance(eitem, list):
                            for eidx, entity in enumerate(eitem):
                                result['aircrafts'][idx]['airspace']['entities'][key][eidx]['attributes'] = resolve_e5x_payload(f'E5X.Occurrence.AirSpace', entity['attributes'])
                        else:
                            result['aircrafts'][idx]['airspace']['entities'][key]['attributes'] = resolve_e5x_payload(f'E5X.Occurrence.AirSpace', item['attributes'])

                if 'aerodrome' in result['aircrafts'][idx]:
                    result['aircrafts'][idx]['aerodrome'] = clean_e5x_object(result['aircrafts'][idx]['aerodrome'])
                    # Attributes
                    for key, item in result['aircrafts'][idx]['aerodrome'].get('attributes', {}).items():
                        result['aircrafts'][idx]['aerodrome']['attributes'][key] = resolve_e5x_payload(f'E5X.Occurrence.Aerodrome', {key: item})
                    # Entities
                    for key, item in result['aircrafts'][idx]['aerodrome'].get('entities', {}).items():
                        if isinstance(eitem, list):
                            for eidx, entity in enumerate(eitem):
                                result['aircrafts'][idx]['aerodrome']['entities'][key][eidx]['attributes'] = resolve_e5x_payload(f'E5X.Occurrence.Aerodrome', entity['attributes'])
                        else:
                            result['aircrafts'][idx]['aerodrome']['entities'][key]['attributes'] = resolve_e5x_payload(f'E5X.Occurrence.Aerodrome', item['attributes'])

                    #for key, item in result['aircrafts'][idx]['aircraft']['e5x'].get('aerodrome', {}).items():
                    #    result['aircrafts'][idx]['aircraft']['e5x']['aerodrome'][key] = resolve_e5x_payload(f'E5X.Occurrence.Aircraft.{key}', {key: item})
                if 'occurrence' in result['aircrafts'][idx]:
                    result['aircrafts'][idx]['occurrence'] = clean_e5x_object(result['aircrafts'][idx]['occurrence'])
                    for key, item in result['aircrafts'][idx].get('occurrence', {}).items():
                        result['aircrafts'][idx]['occurrence'][key] = resolve_e5x_payload(f'E5X.Occurrence.Aircraft', {key: item})
            result['_id'] = str(result['_id'])

            return eve_response(result, 200)
        else:
            return eve_response({'activity': activity, 'obsreg_id': obsreg_id, 'obsreg': None}, 404)

    except Exception as e:
        app.logger.exception('Error fetching obsreg for activity {} and obsreg_id {}'.format(activity, obsreg_id))

    return eve_response({'activity': activity, 'obsreg_id': obsreg_id, 'obsreg': None}, 500)


@Lungo.route("/obsreg/e5x/attributes", methods=['GET'])
@require_client_access_token()
def reverse_get_e5x_attributes():
    driver = app.data.driver
    col = driver.db['e5x_attributes']
    try:
        parsed = parse_request(resource='e5x_attributes', is_blueprint=False, trigger_hooks=False)
        if 'where' not in parsed:
            parsed['where'] = {}
        parsed['where']['rit_version'] = RIT_VERSION
        results = list(execute_parsed_query(collection=get_data_driver(collection_name='e5x_attributes'), parsed=parsed))

        return eve_response(results, 200)

    except Exception as e:
        app.logger.exception('Error fetching attributes')

    return abort(500)


@Lungo.route("/obsreg/e5x/choices", methods=['GET'])
@require_client_access_token()
def reverse_get_e5x_choices():
    driver = app.data.driver
    col = driver.db['e5x_choices']
    try:
        parsed = parse_request(resource='e5x_choices', is_blueprint=False, trigger_hooks=False)
        if 'where' not in parsed:
            parsed['where'] = {}
        parsed['where']['rit_version'] = RIT_VERSION
        results = list(execute_parsed_query(collection=get_data_driver(collection_name='e5x_choices'), parsed=parsed))

        return eve_response(results, 200)

    except Exception as e:
        app.logger.exception('Error fetching choices')

    return abort(500)


@Lungo.route("/obsreg/e5x/choices/<int:_id>", methods=['GET'])
@require_client_access_token()
def reverse_get_e5x_choice():
    driver = app.data.driver
    col = driver.db['e5x_choices']
    try:
        parsed = parse_request(resource='e5x_choices', is_blueprint=False, trigger_hooks=False)
        if 'where' not in parsed:
            parsed['where'] = {}
        parsed['where']['rit_version'] = RIT_VERSION
        results = list(execute_parsed_query(collection=get_data_driver(collection_name='e5x_choices'), parsed=parsed))

        return eve_response(results, 200)

    except Exception as e:
        app.logger.exception('Error fetching choices')

    return abort(500)
