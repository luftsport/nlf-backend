"""
Lungo functions defined here
"""
import requests
from ext.scf import LUNGO_HEADERS, LUNGO_URL


def get_person(person_id) -> (bool, dict):
    resp = requests.get('{}/persons/{}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS)

    if resp.status_code == 200:
        return True, resp.json()

    return False, None


def get_person_acl(person_id) -> (bool, dict):
    acl = []
    resp = requests.get('{}/acl/{}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS)

    if resp.status_code == 200:
        r = resp.json()

        # Prepare acl roles
        for item in r.get('_items', []):
            # print(item)
            acl.append(item)
            acl.append({
                'activity': item['activity'],
                'org': 0,
                'role': item['role'],
                'type': item['type']
            })
            acl.append({
                'activity': 0,
                'org': 0,
                'role': item['role'],
                'type': item['type']
            })

        return True, acl

    return False, None


def get_person_acl_simple(person_id) -> (bool, dict):
    acl = []
    resp = requests.get('{}/acl/simple/{}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS)

    if resp.status_code == 200:
        r = resp.json()


def get_person_activities(person_id):
    activities = []
    resp = requests.get('{}/acl/activities/{}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS)

    if resp.status_code == 200:

        r = resp.json()
        if '_items' in r:
            activities = r['_items']

        return True, activities

    return False, None


def get_person_merged_from(person_id):
    merged_from = []

    resp = requests.get('%s/persons/merged?aggregate={"$person_id":%s}' % (LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS)

    if resp.status_code == 200:
        r = resp.json()
        if '_item' in r and len(r['_items']) == 1:
            return r.get('_items', [{}])[0].get('merged_from', [])

        return True, merged_from

    return False, None


def get_person_from_role(role) -> (bool, [int]):
    resp = requests.get(
        '%s/functions?where={"active_in_org_id": %i, "type_id": %i}&projection={"person_id": 1}'
        % (LUNGO_URL, role.get('club'), role.get('role')),
        headers=LUNGO_HEADERS)

    if resp.status_code == 200:
        r = resp.json()
        if '_items' in r:
            if len(r['_items']) == 1:
                return True, [r['_items'][0]['person_id']]
            elif len(r['_items']) > 1:
                return True, [i['person_id'] for i in r['_items']]

    return False, None
