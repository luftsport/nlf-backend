from flask import current_app as app
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
        if person in self.persons:
            return -1 * (self.persons.index(person) + 1)
        else:
            self.persons.append(person)
            # self.persons = list(set(self.persons))
            return -1 * (self.persons.index(person) + 1)

        return 0

    def assign_x(self, x):
        """Take the whole array part, modify id and tempname, return whole array"""

        if x == None or x == '' or not x:
            return None

        if not 'id' in x:
            x['id'] = 0

        # Allow users to see themself
        if int(x['id']) == int(app.globals['id']):
            # Always delete tmp_name!
            if 'tmp_name' in x:
                del x['tmp_name']
            return x


        elif 'id' in x and 'tmp_name' not in x:
            # print("ID: %s" % x['id'])
            if x['id'] > 0:
                x['id'] = self.assign(x['id'])
            else:
                # print("X her: " % x)
                pass

        elif 'id' in x and 'tmp_name' in x:
            # print("ID TMP: %s %s" % (x['id'], x['tmp_name']))
            if x['id'] > 0:
                x['id'] = self.assign(x['id'])
            else:
                x['id'] = self.assign(x['id'])


        elif 'id' not in x and 'tmp_name' in x:
            # print("TMP: %s" % x['tmp_name'])
            x['id'] = 0  # self.assign(x['tmp_name'])

        else:
            # print("ERROR")
            x['id'] = 0

        # Always delete tmp_name!
        if 'tmp_name' in x:
            del x['tmp_name']

        # print("NEW: %s" % x['id'])
        return x

    def assign_pair(self, x):
        return self.assign_x(x)


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

    # Remove keys
    item.pop('acl', None)

    if 'audit' not in item.get('workflow', {}):
        item['workflow']['audit'] = []

    if 'involved' not in item:
        item['involved'] = []

    if 'components' not in item:
        item['components'] = []

    # ASK MACRO anon
    for ask_key in list(item.get('ask', {}).get('text', {}).keys()):

        try:

            soup = BeautifulSoup(item.get('ask', {}).get('text', {}).get(ask_key, ''), features='html.parser')
            macros = soup.findAll('macro')
            for key, macro in enumerate(macros):

                # USER MACRO
                if macros[key].get('data-type', '') == 'user' and int(macros[key].get('data-id', 0)) != int(app.globals['id']):

                    macros[key]['data-id'] = anon.assign_pair({'id': int(macros[key].get('data-id', 0))}).get('id', 0)

                    macros[key].string = '{} {}'.format(preamble, -1*macros[key].get('data-id'))

                    for attr in list(macros[key].attrs.keys()):
                        if attr not in ['data-id', 'data-type']:
                            macros[key].attrs.pop(attr, None)

                    macros[key]['class'] = 'anon'
                    macros[key]['data-id'] = '#'

                item['ask']['text'][ask_key] = '{}'.format(soup)

        except Exception as e:

            item['ask']['text'][ask_key] = '<macro>Anon Error ({})</macro>'.format(e)

    # Aircraft CREW
    for key, aircraft in enumerate(item.get('aircrafts', [])):
        try:
            for k, crew in enumerate(aircraft.get('crew', [])):
                item['aircrafts'][key]['crew'][k]['person'] = anon.assign_pair(item['aircrafts'][key]['crew'][k].get('person', {}))
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

            # Involved.gear -> rigger
            if 'gear' in item['involved'][key]:  # ".get('gear', False):
                if 'rigger' in item['involved'][key]['gear']:  # .get('rigger', False):
                    item['involved'][key]['gear']['rigger'] = anon.assign_pair(
                        item['involved'][key]['gear'].get('rigger', 0))

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

        if 'hfl' in item['organization']:  # if item['organization'].get('hfl', False):
            for k, hfl in enumerate(item['organization']['hfl']):
                item['organization']['hfl'][k] = anon.assign_pair(item['organization']['hfl'][k])

        if 'hm' in item['organization']:  # if item['organization'].get('hm', False):
            for k, hm in enumerate(item['organization']['hm']):
                item['organization']['hm'][k] = anon.assign_pair(item['organization']['hm'][k])

        if 'pilot' in item['organization']:  # if item['organization'].get('pilot', False):
            for k, pilot in enumerate(item['organization']['pilot']):
                item['organization']['pilot'][k] = anon.assign_pair(item['organization']['pilot'][k])

    # Files
    try:
        item['files'][:] = [d for d in item['files'] if d.get('r') != True]
    except Exception as e:
        item['files'] = None
        app.logger.info("File error: {}".format(e))
        pass

    # Workflow audit trail
    if item.get('workflow', False):
        if item['workflow'].get('audit', False):
            for key, val in enumerate(item['workflow']['audit']):

                if item['workflow']['audit'][key]:

                    if item['workflow']['audit'][key]['a'] in ['init', 'set_ready', 'send_to_hi', 'withdraw']:
                        item['workflow']['audit'][key]['u'] = anon.assign(item['workflow']['audit'][key]['u'])

    # Reporter AND owner
    if 'reporter' in item:
        item['reporter'] = anon.assign(item['reporter'])
    if 'owner' in item:
        item['owner'] = anon.assign(item['owner'])

    return item


"""
except:
    eve_abort(500, 'Server experienced problems (Anon) anonymousing the observation and aborted as a safety measure')
    return {}
"""


def has_permission_obs(id, type):
    """ Checks if has type (execute, read, write) permissions on an observation or not
    Only for after_get_observation
    @note: checks on list comprehension and returns number of intersects in list => len(list) > 0 == True
    @bug: Possible bug if user comparison is int vs float!
    @todo: Should not be execute rights? Or could it be another type 'noanon' or if in users with read right? 
    """

    return acl_helper.has_permission(ObjectId(id), type, 'observations')

    return False
