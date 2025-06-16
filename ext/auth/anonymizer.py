from flask import g, current_app as app
from bson.objectid import ObjectId
import ext.auth.acl as acl_helper
from ext.app.eve_helper import eve_abort
import sys
from pprint import pprint
from bs4 import BeautifulSoup


class Anon(object):
    def __init__(self):
        self.persons = []

    def assign(self, person):
        """Keep track of all assigned persons"""

        # See yourself
        if int(person) == int(g.user_id):
            return int(person)

        if person in self.persons:
            return -1 * (self.persons.index(person) + 1)
        else:
            self.persons.append(person)
            # self.persons = list(set(self.persons))
            return -1 * (self.persons.index(person) + 1)

        return 0

    def assign_x(self, x):
        """Take the whole array part, modify id and tempname, return whole array"""

        if x is None or x == '' or not x:
            return None

        if 'id' not in x:
            x['id'] = 0

        # Allow users to see themself
        if int(x['id']) == int(g.user_id):
            # Always delete tmp_ and full_name!
            x.pop('tmp_name', None)
            x.pop('full_name', None)

            return x


        elif 'id' in x and 'tmp_name' not in x:
            if x['id'] > 0:
                x['id'] = self.assign(x['id'])
            else:
                pass

        elif 'id' in x and 'tmp_name' in x:
            if x['id'] > 0:
                x['id'] = self.assign(x['id'])
            else:
                x['id'] = self.assign(x['id'])


        elif 'id' not in x and 'tmp_name' in x:
            x['id'] = 0  # self.assign(x['tmp_name'])

        else:
            x['id'] = 0

        # Always delete tmp_ and full_name!
        x.pop('tmp_name', None)
        x.pop('full_name', None)

        return x

    def assign_pair(self, x):
        return self.assign_x(x)

class AnonAircraft(object):

    def __init__(self):
        self.aircraft = []

    def assign(self, aircraft):
        """Keep track of all assigned persons"""

        if aircraft in self.aircraft:
            return "FLY-{}".format(self.aircraft.index(aircraft) + 1)
        else:
            self.aircraft.append(aircraft)
            return "FLY-{}".format(self.aircraft.index(aircraft) + 1)

        return "FLY-0"

def _anon_membership_payment(payment):
    try:
        return {'year': payment.get('year', None), 'type': payment.get('type', None)}
    except:
        pass

    return None


def _remove_from_person_data(item):
    """Removes possible traceble id's in person object"""

    # Functions - list of id's
    # item.pop('functions', None)
    item['functions'] = []

    # Competences
    try:
        item['competences'] = [
            {
                '_code': d['_code'],
                'expiry': d['expiry']
            } for d in item['competences']
        ]
    except:
        item['competences'] = []

    # Licenses
    try:
        item['licenses'] = [
            {
                'type_id': d['type_id'],
                'expiry': d['expiry'],
                'status_date': d['status_date']
            } for d in item['licenses']
        ]
    except:
        item['licenses'] = []

    # memberships
    try:
        item['memberships'] = [
            {
                'club': d['club'],
                'discipline': d['discipline'],
                'activity': d['activity'],
                'from_date': d['from_date'],
                'payment': _anon_membership_payment(d['payment'])
            } for d in item['memberships']
        ]
    except:
        item['memberships'] = []

    # magazines
    try:
        item['magazines'] = [{'name': d['name'], 'year': d['year']} for d in item['magazines']]
    except:
        item['magazines'] = []

    # federation (not used as of now)
    try:
        item['federation'] = [
            {
                'activity': d['activity'],
                'year': d['year'],
                'type': d['type'],
                'paid': d['paid'],
            } for d in item['federation']
        ]
    except:
        # item['federation'] = []
        pass

    return item

def anonymize_ors(item):
    """ Anonymizes based on a simple scheme
    Only for after_get_observation
    Should see if solution to have association of user id to a fixed (negative) number for that id to be sorted as "jumper 1", "jumper 2" etc in frontend
    @todo: remove anon files from list 
    @todo: add check for nanon's (non-anon) which should return item directly
    @todo: see if you are involved then do not anon that?
    @todo: for workflow see if all involved should be added to nanon or seperate logic to handle that?
    @todo: add "hopper 1" "hopper 2" etc involved[45199] = -3

        try:
                item['involved'][key] = anon.assign_pair(item['involved'][key])

            except KeyError:
                app.logger.info("Keyerr 1")
                pass
            except:
                app.logger.info("Unexpected error 1: %s" % sys.exc_info()[0])
                pass
    """

    # Set preamble
    """
    if item.get('_model', {}).get('type') == 'fallskjerm':
        preamble = 'Hopper'
    elif item.get('_model', {}).get('type') == 'motorfly':
        preamble = 'Flyver'
    """
    preamble = 'Person'
    # try:
    anon = Anon()
    anon_aircraft = AnonAircraft()

    # Remove keys
    item.pop('acl', None)

    if 'audit' not in item.get('workflow', {}):
        item['workflow']['audit'] = []

    if 'involved' not in item:
        item['involved'] = []

    if 'components' not in item:
        item['components'] = []

    # Remove LEGACY
    item.pop('watchers', None)

    # ASK MACRO anon
    for ask_key in list(item.get('ask', {}).get('text', {}).keys()):

        try:

            soup = BeautifulSoup(item.get('ask', {}).get('text', {}).get(ask_key, ''), features='html.parser')
            macros = soup.findAll('macro')
            for key, macro in enumerate(macros):

                # USER MACRO
                if macros[key].get('data-type', '') == 'user' and int(macros[key].get('data-id', 0)) != int(
                        g.user_id):

                    macros[key]['data-id'] = anon.assign_pair({'id': int(macros[key].get('data-id', 0))}).get('id', 0)

                    macros[key].string = '{} {}'.format(preamble, -1 * macros[key].get('data-id'))

                    for attr in list(macros[key].attrs.keys()):
                        if attr not in ['data-id', 'data-type']:
                            macros[key].attrs.pop(attr, None)

                    macros[key]['class'] = 'anon'
                    macros[key]['data-id'] = '#'

                item['ask']['text'][ask_key] = '{}'.format(soup)

        except Exception as e:

            item['ask']['text'][ask_key] = '<macro>Anon Error ({})</macro>'.format(e)

    # Aircraft CREW and AIRCRAFT
    for key, aircraft in enumerate(item.get('aircrafts', [])):

        try:
            item['aircrafts'][key]['aircraft'].pop('_id', None)
            item['aircrafts'][key]['aircraft']['msn'] = 'msn-anon'  # .pop('msn', None)
            item['aircrafts'][key]['aircraft']['callsign'] = anon_aircraft.assign(item['aircrafts'][key]['aircraft']['callsign'])
        except Exception as e:
            pass

        try:
            if 'e5x' in item['aircrafts'][key]['aircraft']:
                item['aircrafts'][key]['aircraft']['e5x']['attributes']['callsign'] = anon_aircraft.assign(item['aircrafts'][key]['aircraft']['e5x']['attributes']['callsign'])
                item['aircrafts'][key]['aircraft']['e5x']['attributes']['aircraftRegistration']['value'] = anon_aircraft.assign(item['aircrafts'][key]['aircraft']['e5x']['attributes']['aircraftRegistration']['value'])
                item['aircrafts'][key]['aircraft']['e5x']['attributes']['serialNumber']['value'] = 'serial-anon'
        except Exception as e:
            item['aircrafts'][key]['aircraft']['e5x']['attributes'].pop('callsign', None)
            item['aircrafts'][key]['aircraft']['e5x']['attributes'].pop('aircraftRegistration', None)
            item['aircrafts'][key]['aircraft']['e5x']['attributes'].pop('serialNumber', None)

        try:
            for k, crew in enumerate(aircraft.get('crew', [])):
                item['aircrafts'][key]['crew'][k]['person'] = anon.assign_pair(
                    item['aircrafts'][key]['crew'][k].get('person', {}))

                if 'data' in item['aircrafts'][key]['crew'][k].get('person', {}):
                    item['aircrafts'][key]['crew'][k]['person']['data'] = _remove_from_person_data(item['aircrafts'][key]['crew'][k]['person']['data'])
        except Exception as e:
            pass

    # E5X audit
    for key, audit in enumerate(item.get('e5x', {}).get('audit', [])):
        try:
            item['e5x']['audit'][key]['person_id'] = anon.assign(item['e5x']['audit'][key].get('person_id', 0))
        except Exception as e:
            pass

    # Involved
    for key, val in enumerate(item.get('involved', [])):

        if item['involved'][key] == None or item['involved'][key] == '' or not item['involved'][key]:
            item['involved'][key] = None

        else:
            item['involved'][key] = anon.assign_pair(item['involved'][key])

            if 'data' in item['involved'][key]:
                item['involved'][key]['data'] = _remove_from_person_data(item['involved'][key]['data'])

            # Involved.gear -> rigger
            if 'gear' in item['involved'][key].get('data', {}):  # ".get('gear', False):
                if 'rigger' in item['involved'][key]['data']['gear']:  # .get('rigger', False):
                    try:
                        item['involved'][key]['data']['gear']['rigger'] = anon.assign_pair(
                            item['involved'][key]['data']['gear'].get('rigger', {'id': 0}))

                        if 'data' in item['involved'][key]['data']['gear']['rigger']:
                            item['involved'][key]['data']['gear']['rigger']['data'] = _remove_from_person_data(item['involved'][key]['data']['gear']['rigger']['data'])
                    except:
                        item['involved'][key]['data']['gear'].pop('rigger', None)

    # Involved in components
    for key, val in enumerate(item.get('components', [])):

        if item['components'][key] == None or item['components'][key] == '' or not item['components'][key]:
            item['components'][key] = None
        else:
            for k, v in enumerate(item['components'][key]['involved']):
                item['components'][key]['involved'][k] = anon.assign_pair(item['components'][key]['involved'][k])

    # Organization
    if 'organization' in item:

        if 'hl' in item['organization']:  # .get('hl', False):
            for k, hl in enumerate(item['organization']['hl']):
                item['organization']['hl'][k] = anon.assign_pair(item['organization']['hl'][k])

                if 'data' in item['organization']['hl'][k]:
                    item['organization']['hl'][k]['data'] = _remove_from_person_data(item['organization']['hl'][k]['data'])

        if 'hfl' in item['organization']:  # if item['organization'].get('hfl', False):
            for k, hfl in enumerate(item['organization']['hfl']):
                item['organization']['hfl'][k] = anon.assign_pair(item['organization']['hfl'][k])

                if 'data' in item['organization']['hfl'][k]:
                    item['organization']['hfl'][k]['data'] = _remove_from_person_data(item['organization']['hfl'][k]['data'])

        if 'hm' in item['organization']:  # if item['organization'].get('hm', False):
            for k, hm in enumerate(item['organization']['hm']):
                item['organization']['hm'][k] = anon.assign_pair(item['organization']['hm'][k])

                if 'data' in item['organization']['hm'][k]:
                    item['organization']['hm'][k]['data'] = _remove_from_person_data(item['organization']['hm'][k]['data'])

        if 'pilot' in item['organization']:  # if item['organization'].get('pilot', False):
            for k, pilot in enumerate(item['organization']['pilot']):
                item['organization']['pilot'][k] = anon.assign_pair(item['organization']['pilot'][k])

                if 'data' in item['organization']['pilot'][k]:
                    item['organization']['pilot'][k]['data'] = _remove_from_person_data(item['organization']['pilot'][k]['data'])

    # Files
    try:
        item['files'][:] = [d for d in item['files'] if d.get('r') != True]
    except Exception as e:
        item['files'] = []
        app.logger.info("File error: {}".format(e))
        pass

    # Workflow audit trail
    if item.get('workflow', False):
        if item['workflow'].get('audit', False):
            for key, val in enumerate(item['workflow']['audit']):

                if item['workflow']['audit'][key]:

                    if item['workflow']['audit'][key]['a'] in ['init', 'set_ready', 'send_to_hi', 'send_to_ors', 'withdraw']:
                        item['workflow']['audit'][key]['u'] = anon.assign(item['workflow']['audit'][key]['u'])

    # Reporter AND owner
    if 'reporter' in item:
        item['reporter'] = anon.assign(item['reporter'])
    if 'owner' in item:
        item['owner'] = anon.assign(item['owner'])

    return item
