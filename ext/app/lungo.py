"""
Lungo functions defined here
"""
import requests
from ext.scf import LUNGO_HEADERS, LUNGO_URL

# To be able to use this standalone
from flask import current_app as app
try:
    if app.coni
except:
    app = {'config': {'REQUESTS_VERIFY': False}}


def get_person(person_id) -> (bool, dict):
    resp = requests.get('{}/persons/{}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS,
                        verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:
        return True, resp.json()

    return False, None


def get_person_acl(person_id) -> (bool, dict):
    acl = []
    resp = requests.get('{}/acl/{}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS,
                        verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:
        r = resp.json()

        # Prepare acl roles
        for item in r.get('_items', []):
            # print(item)
            acl.append(item)
            # All orgs
            acl.append({
                'activity': item['activity'],
                'org': 0,
                'role': item['role'],
                'type': item['type']
            })
            # All org and activity
            acl.append({
                'activity': 0,
                'org': 0,
                'role': item['role'],
                'type': item['type']
            })

        # return True, [{'activity': a['activity'], 'org': a['org'], 'role': a['role']} for a in acl]
        return True, acl

    return False, None


def get_person_acl_simple(person_id) -> (bool, dict):
    acl = []
    resp = requests.get('{}/acl/simple/{}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS,
                        verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:
        r = resp.json()


def get_person_activities(person_id):
    activities = []
    resp = requests.get('{}/acl/activities/{}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS,
                        verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:

        r = resp.json()
        if '_items' in r:
            activities = r['_items']

        return True, activities

    return False, None


def get_person_merged_from(person_id):
    merged_from = []

    resp = requests.get('%s/persons/merged?aggregate={"$person_id":%s}' % (LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS,
                        verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:
        r = resp.json()
        if '_item' in r and len(r['_items']) == 1:
            return r.get('_items', [{}])[0].get('merged_from', [])

        return True, merged_from

    return False, None


def get_person_from_role(role) -> (bool, [int]):
    resp = requests.get(
        '%s/functions?where={"active_in_org_id": %s, "type_id": %s, "is_deleted": false, "is_passive": false}&projection={"person_id": 1}'
        % (LUNGO_URL, role.get('org'), role.get('role')),
        headers=LUNGO_HEADERS, verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:
        r = resp.json()
        if '_items' in r:
            if len(r['_items']) == 1:
                return True, [r['_items'][0]['person_id']]
            elif len(r['_items']) > 1:
                return True, [i['person_id'] for i in r['_items']]

    return False, None


def get_person_email(person_id) -> (bool, dict):
    resp = requests.get('{}/persons/{}?projection={{"full_name": 1, "address.email": 1}}'.format(LUNGO_URL, person_id),
                        headers=LUNGO_HEADERS,
                        verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:
        r = resp.json()
        email = r.get('address', {}).get('email', [])[0]
        name = r.get('full_name', '')
        return True, {'full_name': name, 'email': email}

    return False, None


def get_org_name(org_id):
    print('{}/{}/{}'.format(LUNGO_URL, 'organizations', org_id))
    resp = requests.get('{}/{}/{}?projection={{"name": 1}}'.format(LUNGO_URL, 'organizations', org_id),
                        headers=LUNGO_HEADERS,
                        verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:
        return True, resp.json().get('name', 'Ukjent Klubb')

    return False, 'Ukjent klubb'


def get_person_name(person_id):
    resp = requests.get('{}/{}/{}?projection={{"full_name": 1}}'.format(LUNGO_URL, 'persons', person_id),
                        headers=LUNGO_HEADERS,
                        verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:
        return True, resp.json().get('full_name', 'Ukjent person')

    return False, 'Ukjent person'


def get_orgs_in_activivity(activity_id, org_type_ids=[6, 14, 19]):
    """
    Aggregation
    :param activity_id:
    :param org_type_ids:
    :return:
    """
    resp = requests.get(
        '{}/organizations/activity?aggregate={{"$activity": {}, "$type_ids": {}}}'.format(LUNGO_URL,
                                                                                          activity_id,
                                                                                          org_type_ids),
        headers=LUNGO_HEADERS,
        verify=app['config'].get('REQUESTS_VERIFY', True))

    if resp.status_code == 200:
        try:
            print(resp.json())
            return resp.json().get('_items', [{}])[0].get('org_ids', [])
        except IndexError as e:
            pass

    print(resp.text)
    return []


def get_users_from_role(type_id, org_type_ids=[6, 14, 19]):
    """
    Get person_ids from a role
    :param type_id:
    :param org_type_ids:
    :return:
    """
    resp = requests.get(
        '{}/functions/persons?aggregate={{"$type_id": {}, "$org_ids": {}}}'.format(LUNGO_URL,
                                                                                   type_id,
                                                                                   org_type_ids),
        headers=LUNGO_HEADERS,
        # verify=app['config'].get('REQUESTS_VERIFY', True)
    )

    if resp.status_code == 200:
        try:
            print(resp.json())
            return resp.json().get('_items', [{}])[0].get('person_ids', [])
        except IndexError as e:
            pass

    print(resp.text)
    return []


def get_recepient(person_id):
    return get_recepients([person_id])


def get_recepients(recepients):
    persons = []

    try:
        query = 'where={{"id": {{"$in": {} }}}}&projection={{"full_name": 1, "address.email": 1}}'.format(recepients)
        print('{}/{}?{}'.format(LUNGO_URL, 'persons', query))
        resp = requests.get('{}/{}?{}'.format(LUNGO_URL, 'persons', query), headers=LUNGO_HEADERS)

        if resp.status_code == 200:

            for person in resp.json()['_items']:
                if not '_merged_to' in person:
                    try:
                        persons.append({
                            'full_name': person.get('full_name', ''),
                            'email': person.get('address', {}).get('email', [])[0]})
                    except Exception as e:
                        pass

        return list({v['email']: v for v in persons if len(v['email']) > 4}.values())

    except:
        pass

    return persons


def get_recepients_from_roles(roles):
    persons = []

    try:
        for role in roles:
            resp = requests.get(
                '{}/functions?where={{"org_id": {}, "type_id": {}, "is_deleted": false, "is_passive": false }}&projection={{"person_id": 1}}'.format(
                    LUNGO_URL, role.get('org', 0), role.get('role', 0)),
                headers=LUNGO_HEADERS)

            if resp.status_code == 200:
                for item in resp.json().get('_items', []):
                    persons.append(item.get('person_id', 0))

        return get_recepients(list(set([i for i in persons if i > 0])))
    except:
        pass

    return persons
