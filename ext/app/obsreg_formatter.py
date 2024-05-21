TYPES = {
        'sharing': 'Erfaringsdeling',
        'unwanted_act':'Uønsket',
        'unsafe_act':'Utrygg adferd',
        'unsafe_condition':'Utrygge forhold',
        'near_miss':'Næruhell',
        'incident': 'Uhell',
        'accident': 'Ulykke'
}

ATTRIBUTES = {
          'reserve_ride': 'Reserve benyttet',
          'aad_fire': 'Nødåpner fyring' ,
          'aad_rescue':'Nødåpner redning' ,
          'packing_error': 'Pakkefeil' ,
          'gear_malfunction':'Feilfunksjon' ,
          'damage': 'Matriell skade' ,
          'gear_failure': 'Utstyrsvikt' ,
          'rigger_error': 'MK/MR Feil' ,
          'violation': 'Regelbrudd',
          'willful_violation':'Med vitende vilje' ,
          'injury': 'Personskade' ,
          'death': 'Død'
        }

from collections.abc import Iterable
from ext.app.lungo import get_person, get_org_name
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# Ok
def get_org(org_id):
    if org_id < 0:
        return org_id
    status, org_name = get_org_name(org_id)
    if status is True:
        return org_name
    return 'Ukjent'
# Ok
def get_name(person_id):
    if person_id < 0:
        return person_id
    status, person = get_person(person_id)
    if status is True:
        return person.get('full_name', 'Ukjent')
    return 'Ukjent'

def deep_omit(d, keys):
    if isinstance(d, dict):
        for k in keys:
            d.pop(k, None)
        for v in d.values():
            deep_omit(v, keys)
    elif isinstance(d, Iterable) and not isinstance(d, str):
        for e in d:
            deep_omit(e, keys)

    return d

def mgm_attr(components):
    attrs = []
    for c in components:
        for a in c['attributes']:
            attrs.append(a)
    return list(set(attrs))


def causes(components):
    attrs = []
    rcause = None
    incident = None
    fcons = None

    try:
        rcause = components[0]['what']  # if components[0]['flags']['cause'] is True else None
    except:
        pass
    try:
        fcons = components[-1]['what']  # if components[-1]['flags']['consequence'] is True else None
    except:
        pass

    try:
        for c in components:
            if incident is None and c.get('flags', {}).get('incident', False) is True:
                incident = c.get('what', '')

            for key, value in c['attributes'].items():
                if value is True:
                    attrs.append(key)
    except:
        pass

    return rcause, incident, fcons, list(set(attrs))

def get_type(type_key):
    return TYPES.get(type_key, 'Unknown')

def anon_macro(text, anon=None):
    raise NotImplemented
    try:

        soup = BeautifulSoup(text, features='html.parser')
        macros = soup.findAll('macro')
        for key, macro in enumerate(macros):
            # USER MACRO
            macros[key]['data-id'] = anon.get_anon(int(macros[key].get('data-id', 0)))

            macros[key].string = '{} {}'.format(preamble, -1 * macros[key].get('data-id'))

            for attr in list(macros[key].attrs.keys()):
                if attr not in ['data-id', 'data-type']:
                    macros[key].attrs.pop(attr, None)

            macros[key]['class'] = 'anon'
            macros[key]['data-id'] = '#'

        return '{}'.format(soup)

    except Exception as e:

        return '<macro>Anon Error ({})</macro>'.format(e)

    return text
def _format_components(components):
    response = ''
    n = 1
    for component in components:
        try:

            response += '{}. Hvem: {} Hva: {} Hvor: {} Hvordan: {} Attributes: {}\r\n'.format(
                n,
                ' '.join([get_name(x['id']) for x in component['involved']]) or '',
                component.get('what', '') or '',
                component.get('where', {}).get('at', '') + ' ' + str(
                    component.get('where', {}).get('altitude', '')) + 'ft' or '',
                component.get('how', '') or '',
                ' '.join([ATTRIBUTES[key] for key in list(component['attributes'].keys()) if
                          component['attributes'][key] is True])
            )
        except Exception as e:
            print('[ERR] error', e)
            print('Component:')
            print(component)
            response += '{}. Hvem: {} Hva: {} Hvordan: {}'.format(
                n,
                ' '.join([get_name(x['id']) for x in component['involved']]) or '',
                component.get('what', '') or '',
                component.get('how', '') or ''
            )
        n += 1
    return response
def who_closed_it(ors):
    try:
        return get_name(ors['workflow']['audit'][0]['u'])
    except:
        pass

    return 'Unknown or nobody'


def _format_involved():
    pass


def _format_weather():
    pass


class Anon:
    users = []

    def _add_user(self, person_id):
        self.users.append(person_id)

    def get_anon(self, person_id):
        if person_id not in self.users:
            self._add_user(person_id)

        return self.users.index(person_id)

def format_ors(observations, format='dataframe'):

    o = []
    for ors in observations:
        try:
            rcause, incident, conseq, attrs = causes(ors['components'])
            o.append({'id': ors['id'],
                      'title': ' '.join(ors['tags']),
                      'type': get_type(ors.get('type', None)),
                      'status': ors['workflow']['state'],
                      'closed_by': who_closed_it(ors),
                      'when': ors['when'],
                      'where': ors.get('location', {}).get('name', 'Unknown'),
                      'reporter': get_name(ors['reporter']),
                      'club': ors['club'],
                      'club_name': get_org(ors['club']),
                      'involved': ors['involved'],
                      'rating_actual': ors.get('rating', {}).get('actual', 'None'),
                      'rating_potential': ors.get('rating', {}).get('potential', 'None'),
                      'rating_calculated': ors.get('rating', {}).get('_rating', 'None'),
                      'flags': ors.get('flags', []),
                      'components': ors['components'],
                      'components_unpk': _format_components( ors['components']),
                      'root_cause': rcause,
                      'incident': incident,
                      'final_conseqence': conseq,
                      'attributes': ','.join(attrs),  # mgm_attr(ors['components']),
                      'weather': ors['weather'],
                      'ask_attitude': ors.get('ask', {}).get('attitude', 0),
                      'ask_skills': ors.get('ask', {}).get('skills', 0),
                      'ask_knowledge': ors.get('ask', {}).get('knowledge', 0),
                      'comment_reporter': ors.get('ask', {}).get('text', {}).get('draft', ''),
                      'comment_hi': ors.get('ask', {}).get('text', {}).get('pending_review_hi',''),
                      'comment_fsj': ors.get('ask', {}).get('text', {}).get('pending_review_fs',''),
                      'comment_su': ors.get('ask', {}).get('text', {}).get('pending_review_su', ''),
                      'actions_local': ors.get('actions', {}).get('local', 'None'),
                      'actions_central': ors.get('actions', {}).get('central', 'None')
                      })
        except Exception as e:
            print(ors, e)
    df = pd.DataFrame(o)

    if format == 'dataframe':
        return df
    elif format == 'csv':
        return df.to_csv()