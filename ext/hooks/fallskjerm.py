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

from ext.scf import ACL_FALLSKJERM_HI, ACL_FALLSKJERM_SU_GROUP_LIST, ACL_FALLSKJERM_FSJ
from ext.workflows.fallskjerm_observations import ObservationWorkflow, get_wf_init, get_acl_init, WF_FALLSKJERM_ATTR
from ext.app.seq import increment
from ext.app.lungo import get_person_from_role, get_person, get_org_name
from datetime import datetime
from ext.app.notifications import ors_save, ors_workflow, broadcast
from flask import request, g, make_response, send_file, session


def _del_blacklist(d, blacklist):
    """Deletes all keys not in whitelist, not recursive"""
    if isinstance(d, dict):
        keys = d.copy().keys()
        for k in keys:
            if k in blacklist and d[k] != g.user_id:
                d.pop(k, None)
        return d
    return d


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

    o = []
    import traceback
    for obsreg in observations:
        try:
            rcause, incident, conseq, attrs = causes(obsreg['components'])
            o.append({'id': obsreg['id'],
                      'title': ' '.join(obsreg['tags']),
                      'type': get_type(obsreg.get('type', None)),
                      'status': obsreg['workflow']['state'],
                      'closed_by': who_closed_it(obsreg),
                      'when': obsreg['when'],
                      'where': obsreg.get('location', {}).get('name', 'Unknown'),
                      'reporter': get_name(obsreg['reporter']),
                      'club': obsreg['club'],
                      'club_name': get_org_name(obsreg['club']),
                      'involved': obsreg['involved'],
                      'rating_actual': obsreg.get('rating', {}).get('actual', 'None'),
                      'rating_potential': obsreg.get('rating', {}).get('potential', 'None'),
                      'rating_calculated': obsreg.get('rating', {}).get('_rating', 'None'),
                      'flags': obsreg.get('flags', []),
                      'components': obsreg['components'],
                      'root_cause': rcause,
                      'incident': incident,
                      'final_conseqence': conseq,
                      'attributes': ','.join(attrs),  # mgm_attr(obsreg['components']),
                      'weather': obsreg['weather'],
                      'ask_attitude': obsreg.get('ask', {}).get('attitude', 0),
                      'ask_skills': obsreg.get('ask', {}).get('skills', 0),
                      'ask_knowledge': obsreg.get('ask', {}).get('knowledge', 0),
                      'comment_reporter': obsreg.get('ask', {}).get('text', {}).get('draft', ''),
                      'comment_hi': obsreg.get('ask', {}).get('text', {}).get('pending_review_hi', ''),
                      'comment_fsj': obsreg.get('ask', {}).get('text', {}).get('pending_review_fs', ''),
                      'comment_su': obsreg.get('ask', {}).get('text', {}).get('pending_review_su', ''),
                      'actions_local': obsreg.get('actions', {}).get('local', 'None'),
                      'actions_central': obsreg.get('actions', {}).get('central', 'None')
                      })
        except Exception as e:
            print(obsreg['id'], e, traceback.format_exc())
    print('DADA', o)
    df = pd.DataFrame(o)

    return df


def ors_before_insert(items):
    for item in items:
        ors_before_insert_item(item)


def ors_before_insert_item(item):
    try:
        if 'discipline' in item and item.get('discipline', 0) > 0:

            ors_id = increment('ors_fallskjerm')

            if ors_id:
                item['id'] = ors_id
            else:
                return eve_abort(422, 'Could not create OBSREG, missing increment')

            item['when'] = datetime.utcnow()
            item['reporter'] = g.user_id
            item['owner'] = g.user_id
            item['watchers'] = [g.user_id]
            item['workflow'] = get_wf_init(g.user_id)

            role_hi = ACL_FALLSKJERM_HI.copy()
            role_hi['org'] = item.get('discipline')
            _, hi = get_person_from_role(role_hi)
            item['organization'] = {'hi': hi}

            item['acl'] = get_acl_init(g.user_id, item['discipline'])

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
                    model='fallskjerm',
                    org=response[0].get('discipline', 0)
            ) is False:
                for index, val in enumerate(response):
                    response[index] = anon.anonymize_ors(response[index])
    else:
        ors_after_fetched(response)


def ors_after_fetched_list(response):
    for key, item in enumerate(response.get('_items', [])):
        response['_items'][key] = _ors_after_fetched(item)
    print('############################################')
    print(request.args)
    if 'download' in request.args:
        print(_format_obsreg(response['_items']).to_csv(index=False, header=True, sep=";"))
        tmp = _format_obsreg(response['_items'])
        response['_file'] = tmp.to_csv(index=False, header=True, sep=",", quotechar='"')
        #session["obsreg_filter_result_df"] = _format_obsreg(response['_items']).to_csv(index=False, header=True, sep=";")


def ors_after_fetched(response):
    """ Modify response after GETing an observation
    This hook checks if permission on each observation
    If closed, then it will anonymize each observation wo w or x rights
    """
    response = _ors_after_fetched(response)


def _ors_after_fetched(_response):
    # Just to be sure, we remove all data if anything goes wrong!
    # response.set_data({})
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
                            model='fallskjerm',
                            org=_response[key].get('discipline', 0)
                    ) is False:
                        # _response[key]['acl_user'] = user_persmissions(_response[key]['acl'], 'closed')
                        _response[key] = anon.anonymize_ors(_response[key])


        elif isinstance(_response, dict):
            # _response['acl_user'] = user_persmissions(_response['acl'], _response['workflow']['state'])

            # SocketIO
            # broadcast('Somebody is looking at OBSREG#{}'.format(_response['id']))
            _response['acl_user'] = get_user_acl_mapping(_response['acl'])

            """For item return nanon if roles match hi in club or fs"""
            if _response.get('workflow', False) and 'state' in _response['workflow']:
                if _response['workflow']['state'] == 'closed':

                    if has_nanon_permission(
                            resource_acl=_response.get('acl', []),
                            perm='execute',
                            state='closed',
                            model='fallskjerm',
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
                         'Server experienced problems (unknown) anonymousing the observation and aborted as a safety measure')

    return _response


@require_token()
def ors_before_get_todo(request, lookup):
    lookup.update({
        '$and': [
            {'workflow.state': {'$nin': ['closed', 'withdrawn']}},
            {'$or': [{'acl.execute.users': {'$in': [g.user_id]}},
                     {'acl.execute.roles': {'$in': g.acl.get('roles', [])}}]}
        ]
    })


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


def ors_after_update(updates, original):
    """After DB update, updates is just changed data"""

    # Only when not doing workflow transitions
    if updates.get('workflow', {}).get('state', None) is None:
        if original.get('workflow', {}).get('state', 'original') not in ['closed', 'withdrawn']:
            ors_save(
                recepients=parse_acl_flat(original.get('acl', {}), exclude_current_user=False),
                event_from='fallskjerm_observations',
                event_from_id=original.get('_id', None),
                source=original.get('_version', 1),
                destination=original.get('_version', 2) + 1,
                context='save'
            )


@require_token()
def ors_before_post_comments(resource, items):
    if resource == 'fallskjerm/observation/comments':
        items[0].update({'user': int(g.user_id)})
