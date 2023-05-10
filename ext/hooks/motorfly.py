"""

    Event hooks:
    ============

    Using Eve defined events

    From 0.7 - needs request token?

    Mixed with signals to ext.hooks for flask and direct database access compatibility

    Eve specific hooks are defined according to

    def <resource>_<when>_<method>():

    When attaching to app, remember to use post and pre for request hooks

    @note: all requests are supported: GET, POST, PATCH, PUT, DELETE
    @note: POST (resource, request, payload)
    @note: POST_resource (request, payload)
    @note: GET (resource, request, lookup)
    @note: GET_resource (request, lookup)

"""
import ext.auth.anonymizer as anon
from ext.auth.acl import get_user_acl_mapping, parse_acl_flat, has_nanon_permission
from ext.app.eve_helper import eve_abort
from ext.app.decorators import *
import json

from ext.scf import (
    ACL_MOTORFLY_CLUB_SKOLESJEF,
    ACL_MOTORFLY_ORS,
    ACL_MOTORFLY_CLUB_DTO,
    ACL_MOTORFLY_CLUB_FTL,
    ACL_MOTORFLY_FLYTJENESTEADM
)
from ext.workflows.motorfly_observations import ObservationWorkflow, get_wf_init, get_acl_init
from ext.app.seq import increment
from ext.app.lungo import get_person_from_role, get_person, get_org_name
from datetime import datetime
from ext.app.notifications import ors_save, ors_workflow, broadcast
from ext.hooks.common import cast_choices
from flask import request, g, make_response, send_file, session, current_app as app


def _format_obsreg(observations):
    import pandas as pd
    OBSREG_TYPES = {
        'sharing': 'Erfaringsdeling',
        'unwanted_act': 'Uønsket',
        'unsafe_act': 'Utrygg adferd',
        'unsafe_condition': 'Utrygge forhold',
        'near_miss': 'Næruhell',
        'incident': 'Uhell',
        'accident': 'Ulykke'
    }
    WORKFLOW_STATES = {
        'draft': 'Utkast',
        'pending_review_ors': 'OBSREG Koordinator',
        'pending_review_flytjenesteadm': 'FlytjenesteADM',
        'pending_review_ftl': 'FTL',
        'pending_review_flytjenesten': 'Flytjenesten',
        'pending_review_dto': ' DTO',
        'pending_review_skole': 'Skole',
        'pending_review_operativ': 'Operativ',
        'pending_review_teknisk': 'Teknisk',
        'closed': 'Lukket',
        'withdrawn': 'Trukket'

    }

    def get_type(type_key):
        return OBSREG_TYPES.get(type_key, 'Unknown')


    def who_closed_it(ors):
        try:
            return get_name(ors['workflow']['audit'][0]['u'])
        except:
            pass

        return 'Unknown or nobody'


    def get_name(person_id):
        status, person = get_person(person_id)

        if status is True:
            return person.get('full_name', 'Ukjent person eller anonymisert')

        return 'Ukjent person eller anonymisert'


    def get_state(state_key):
        return WORKFLOW_STATES.get(state_key, 'Unknown')


    def get_narrative(ors):
        try:
            return ors.get('occurrence', {}).get('entities', {}).get('reportingHistory', {})[0].get('attributes', {}).get(
                'reporterSDescription', {}).get('plainText', '')
        except:
            pass

        return ''


    def get_occurence_class(ors):
        classes = {
            100: "Accident",
            200: "Serious Incident",
            300: "Incident",
            301: "Major Incident",
            302: "Significant Incident",
            400: "Occurrence without safety effect",
            500: "Not determined",
            501: "Observation",
            502: "Occurrence with No Flight Intended"

        }
        return classes.get(ors.get('occurence', {}).get('occurenceClass', ''), 'Ukjent')


    def get_detection_phase(ors):
        phases = {
            1: "Manufacturing",
            2: "Scheduled Maintenance",
            3: "Non-scheduled Maintenance",
            4: "Standing",
            5: "Taxi",
            6: "Take-Off",
            8: "En-Route",
            10: "Approach",
            11: "Landing",
            12: "Manoeuvring",
            14: "Unknown",
            15: "Other",
            16: "Post-Impact"
        }


    def get_choice(key, _id_):
        rit_version = "4.1.0.6"
        choices = app.data.driver.db['e5x_choices']

        if isinstance(_id_, list):
            try:
                choices = list(choices.find({'rit_version': rit_version, 'key': key, 'id': {'$in': _id_}},
                                            {'id': 1, 'label': 1}))
                return [x.get('label', 'Ukjent') for x in choices]
            except Exception as e:
                print(key, 'list', e)
                print(choices)
                return []

        else:
            try:
                choice = list(choices.find({'rit_version': rit_version, 'key': key, 'id': _id_}, {'id': 1, 'label': 1}))
                return choice[0].get('label', 'Ukjent')
            except Exception as e:
                print(choice)

        return 'Ukjent'


    import traceback
    o = []
    try:
        for obsreg in observations:
            # if acl in else
            # try:
            # rcause, incident, conseq, attrs = causes(obsreg['components'])
            o.append({'id': obsreg['id'],
                      'title': ' '.join(obsreg['tags']),
                      'type': get_type(obsreg.get('type', None)),
                      'status': get_state(obsreg['workflow']['state']),
                      'closed_by': who_closed_it(obsreg),
                      'when': obsreg['when'],
                      # 'where': obsreg.get('location', {}).get('name', 'Unknown'),
                      'reporter': get_name(obsreg['reporter']),
                      'club': obsreg['club'],
                      'club_name': get_org_name(obsreg['club']),
                      'rating_actual': obsreg.get('rating', {}).get('actual', 'None'),
                      'rating_potential': obsreg.get('rating', {}).get('potential', 'None'),
                      'rating_calculated': obsreg.get('rating', {}).get('_rating', 'None'),
                      # E5X:
                      'OccurrenceClass': get_choice('Occurrence.OccurrenceClass',
                                                    obsreg.get('occurrence', {}).get('attributes', {}).get('occurrenceClass',
                                                                                                        {}).get('value', 0)),
                      'OccurrenceCategory': '\r\n'.join(['{}'.format(x) for x in get_choice('Occurrence.OccurrenceCategory',
                                                                                            obsreg.get('occurrence', {}).get(
                                                                                                'attributes', {}).get(
                                                                                                'occurrenceCategory', {}).get(
                                                                                                'value', []))]),
                      'DetectionPhase': get_choice('Occurrence.DetectionPhase',
                                                   obsreg.get('occurrence', {}).get('attributes', {}).get('detectionPhase',
                                                                                                       {}).get('value', 0)),
                      'HighestDamage': get_choice('Occurrence.HighestDamage',
                                                  obsreg.get('occurrence', {}).get('attributes', {}).get('highestDamage', {}).get(
                                                      'value', 0)),
                      'InjuryLevel': get_choice('Occurrence.InjuryLevel',
                                                obsreg.get('occurrence', {}).get('attributes', {}).get('injuryLevel', {}).get(
                                                    'value', 0)),

                      'flags': obsreg.get('flags', []),
                      'weather': obsreg['weather'],
                      'ask_attitude': obsreg.get('ask', {}).get('attitude', 0),
                      'ask_skills': obsreg.get('ask', {}).get('skills', 0),
                      'ask_knowledge': obsreg.get('ask', {}).get('knowledge', 0),
                      'comment_reporter': obsreg.get('ask', {}).get('text', {}).get('draft', ''),
                      'comment_obsreg': obsreg.get('ask', {}).get('text', {}).get('pending_review_flytjenesteadm', ''),
                      'comment_flytjenesteadm': obsreg.get('ask', {}).get('text', {}).get('pending_review_obsreg', ''),
                      'comment_ftl': obsreg.get('ask', {}).get('text', {}).get('pending_review_ftl', ''),
                      'comment_flytjenesten': obsreg.get('ask', {}).get('text', {}).get('pending_review_flytjenesten', ''),
                      'comment_dto': obsreg.get('ask', {}).get('text', {}).get('pending_review_dto', ''),
                      'comment_skole': obsreg.get('ask', {}).get('text', {}).get('pending_review_skole', ''),
                      'comment_operativ': obsreg.get('ask', {}).get('text', {}).get('pending_review_operativ', ''),
                      'comment_teknisk': obsreg.get('ask', {}).get('text', {}).get('pending_review_teknisk', ''),
                      'actions_local': '\r\n'.join(obsreg.get('actions', {}).get('local', [])),
                      'actions_central': '\r\n'.join(['* {}'.format(x) for x in obsreg.get('actions', {}).get('central', [])]),
                      'reporterSDescription': get_narrative(obsreg)
                      })

    except Exception as e:
        print(obsreg['id'], e, traceback.format_exc())

    df = pd.DataFrame(o)
    return df

def ors_before_insert(items):
    for item in items:
        ors_before_insert_item(item)


def ors_before_insert_item(item):
    try:
        if 'discipline' in item and item.get('discipline', 0) > 0:

            ors_id = increment('ors_motorfly')

            if ors_id:
                item['id'] = ors_id
            else:
                return eve_abort(422, 'Could not create OBSREG, missing increment')

            item['when'] = datetime.utcnow()
            item['reporter'] = g.user_id
            item['owner'] = g.user_id
            item['watchers'] = [g.user_id]
            item['workflow'] = get_wf_init(g.user_id)

            item['organization'] = {}
            _, _person_ors = get_person_from_role(ACL_MOTORFLY_ORS)
            item['organization']['ors'] = _person_ors

            persons_dto = ACL_MOTORFLY_CLUB_DTO.copy()
            persons_dto['org'] = item.get('discipline')
            _, _persons_dto = get_person_from_role(persons_dto)
            item['organization']['dto'] = _persons_dto

            persons_ftl = ACL_MOTORFLY_CLUB_FTL.copy()
            persons_ftl['org'] = item.get('discipline')
            _, _persons_ftl = get_person_from_role(persons_ftl)
            item['organization']['ftl'] = _persons_ftl

            item['acl'] = get_acl_init(g.user_id, item.get('discipline'))


    except Exception as e:
        return eve_abort(422, 'Could not create OBSREG')


def ors_after_inserted(items):
    for item in items:
        ors_after_inserted_item(item)


def ors_after_inserted_item(item):
    wf = ObservationWorkflow(object_id=item.get('_id', ''), user_id=g.user_id)
    if wf.get_current_state().get('state', '') == 'draft':
        wf.notify_created()


def ors_after_fetched_diffs(response):
    if isinstance(response, list):

        if response[0].get('workflow', {}).get('state', None) == 'closed':
            if has_nanon_permission(
                    resource_acl=response[0].get('acl', []),
                    perm='execute',
                    state='closed',
                    model='motorfly',
                    org=response[0].get('discipline', 0)
            ) is False:
                for index, val in enumerate(response):
                    response[index] = anon.anonymize_ors(response[index])
    else:
        ors_after_fetched(response)


def ors_after_fetched_list(response):
    for key, item in enumerate(response.get('_items', [])):
        response['_items'][key] = _ors_after_fetched(item)

    if 'download' in request.args:
        tmp = _format_obsreg(response['_items'])
        response['_file'] = tmp.to_csv(index=False, header=True, sep=",", quotechar='"')


def ors_after_fetched(response):
    """ Modify response after GETing an observation
    This hook checks if permission on each observation
    If closed, then it will anonymize each observation wo w or x rights
    """
    response = _ors_after_fetched(response)


def _ors_after_fetched(_response):
    """ Modify response after GETing an observation
    This hook checks if permission on each observation
    If closed, then it will anonymize each observation wo w or x rights
    """
    # Just to be sure, we remove all data if anything goes wrong!
    # _response.set_data({})
    if isinstance(_response, dict):
        _response['acl_user'] = get_user_acl_mapping(_response.get('acl', {}))
    try:
        if isinstance(_response, list):

            for key, val in enumerate(_response):

                # _response[key]['acl_user'] = user_persmissions(_response[key]['acl'], _response[key]['workflow']['state'])
                _response[key]['acl_user'] = get_user_acl_mapping(_response[key]['acl'])

                if _response[key]['workflow']['state'] == 'closed':

                    if has_nanon_permission(
                            resource_acl=_response[key].get('acl', []),
                            perm='execute',
                            state='closed',
                            model='motorfly',
                            org=_response[key].get('discipline', 0)
                    ) is False:
                        # _response[key]['acl_user'] = user_persmissions(_response[key]['acl'], 'closed')
                        _response[key] = anon.anonymize_ors(_response[key])


        elif isinstance(_response, dict):
            # _response['acl_user'] = user_persmissions(_response['acl'], _response['workflow']['state'])

            _response['acl_user'] = get_user_acl_mapping(_response['acl'])

            """For item return nanon if roles match hi in club or fs"""
            if _response.get('workflow', False) and 'state' in _response['workflow']:
                if _response['workflow']['state'] == 'closed':
                    if has_nanon_permission(
                            resource_acl=_response['acl'],
                            perm='execute',
                            state='closed',
                            model='motorfly',
                            org=_response.get('discipline', 0)
                    ) is False:
                        _response = anon.anonymize_ors(_response)

    except KeyError as e:
        app.logger.info("Keyerror in hook error: {}".format(e))
        return eve_abort(500,
                         'Server experienced problems (keyerror) anonymousing the observation and aborted as a safety measure')
    except Exception as e:
        app.logger.info("Unexpected error: {}".format(e))
        return eve_abort(500,
                         'Server experienced problems (unknown) anonymousing the observation and aborted as a safety measure {}'.format(
                             e))

    return _response


@require_token()
def ors_before_get_todo(request, lookup):
    lookup.update({'$and': [{'workflow.state': {'$nin': ['closed', 'withdrawn']}},
                            {'$or': [{'acl.execute.users': {'$in': [g.user_id]}},
                                     {'acl.execute.roles': {'$in': g.acl.get('roles', [])}}]}]})


@require_token()
def ors_before_get_user(request, lookup):
    lookup.update({'reporter': g.user_id})


@require_token()
def ors_before_get(request, lookup):
    lookup.update({'$or': [{"acl.read.roles": {'$in': g.acl.get('roles', [])}},
                           {"acl.read.users": {'$in': [g.user_id]}}]})


@require_token()
def ors_before_patch(request, lookup):
    lookup.update({'$or': [{"acl.write.roles": {'$in': g.acl.get('roles', [])}},
                           {"acl.write.users": {'$in': [g.user_id]}}]})


def ors_before_update(item, original):
    item = cast_choices(item)


def ors_after_update(updates, original):
    """After DB update, updates is just changed data"""

    # Only when not doing workflow transitions
    if updates.get('workflow', {}).get('state', None) is None:
        if original.get('workflow', {}).get('state', 'original') not in ['closed', 'withdrawn']:
            ors_save(
                recepients=parse_acl_flat(original.get('acl', {}), exclude_current_user=False),
                event_from='motorfly_observations',
                event_from_id=original.get('_id', None),
                source=original.get('_version', 1),
                destination=original.get('_version', 2) + 1,
                context='save'
            )


@require_token()
def ors_before_post_comments(resource, items):
    if resource == 'motorfly/observation/comments':
        items[0].update({'user': int(g.user_id)})
