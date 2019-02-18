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
from ext.auth.acl import get_user_acl_mapping
import ext.app.eve_helper as eve_helper
from ext.app.decorators import *
import json
# import signals from hooks
from ext.hooks.fallskjerm_signals import signal_activity_log, signal_insert_workflow, \
    signal_change_owner, signal_init_acl
from ext.hooks.motor_signals import signal_g_init_acl, signal_g_insert_workflow

from ext.scf import ACL_FALLSKJERM_HI, ACL_FALLSKJERM_SU, ACL_FALLSKJERM_FSJ
from ext.workflows.fallskjerm_observations import get_wf_init, get_acl_init
from ext.app.seq import increment
from ext.app.lungo import get_person_from_role


def ors_before_insert(items):
    """Do everything needed before processing
    Add WF
    Add other known...
    """

    if len(items) > 1:
        eve_abort(401, 'Do not support batch operations')
    elif len(items) == 1:

        try:
            ors = items[0].copy()
            if 'club' in ors and ors.get('club', 0) > 0:

                ors_id = increment('ors_fallskjerm')

                if ors_id:
                    ors['id'] = ors_id
                else:
                    eve_abort(422, 'Could not create ORS, missing increment')

                ors['reporter'] = app.globals.get('user_id')
                ors['owner'] = app.globals.get('user_id')
                ors['watchers'] = [app.globals.get('user_id')]
                ors['workflow'] = get_wf_init(app.globals.get('user_id'))

                role_hi = ACL_FALLSKJERM_HI.copy()
                role_hi['club'] = ors.get('club')
                _, hi = get_person_from_role(role_hi)
                ors['organization'] = {'hi': hi}

                ors['acl'] = get_acl_init(app.globals.get('user_id'), ors['club'])

                items[0] = ors

        except Exception as e:
            print('Error', e)
            pass
    else:
        eve_abort(422, 'Could not create ORS')


def after_g_post(request, response):
    payload = json.loads(response.get_data().decode('UTF-8'))

    signal_g_insert_workflow.send({'app': app, 'payload': payload})

    signal_g_init_acl.send({'app': app, 'payload': payload})


@require_token()
def before_post(request, payload=None):
    pass


def after_patch(request, response):
    """ Change owner, owner is readonly
    """
    signal_change_owner.send(app, response=response)


def after_post(request, response):
    """ When payload as json, request.get_json()
    Else; payload
    @todo: Integrate with ObservationWorkflow!
    @todo: Set expiry as attribute for states!
    """

    payload = json.loads(response.get_data().decode('UTF-8'))

    signal_insert_workflow.send({'app': app, 'payload': payload})

    signal_init_acl.send({'app': app, 'payload': payload})

    # action, ref, user, resource=None ref, act = None, resource=None, **extra

    pass


def after_fetched_p(response, _id):
    print('##### RESPONSE ####')
    print(response)


def after_fetched_diffs(response):
    print('########', response)
    if isinstance(response, list):

        if response[0].get('workflow', {}).get('state', None) == 'closed':
            if has_nanon_permission(response[0].get('acl', []), 'execute', 'closed') is False:
                for index, val in enumerate(response):
                    response[index] = anon.anonymize_ors(response[index])
    else:
        after_fetched(response)


def user_persmissions(resource_acl, state):
    permissions = {
        'read': False,
        'write': False,
        'delete': False,
        'execute': False,
    }

    for perm in permissions.keys():
        permissions[perm] = has_nanon_permission(resource_acl, perm, state)

    return permissions


def has_permission(resource_acl, perm):
    if (
            any(pid for pid in app.globals['acl']['roles'] if pid in resource_acl[perm]['roles']) is True
            or app.globals['user_id'] in resource_acl[perm]['roles'] is True
    ):
        return True
    return False


def has_nanon_permission(resource_acl, perm, state):
    # Closed and should be able to see
    if state == 'closed' and perm == 'execute':
        if (
                any(pid for pid in app.globals['acl']['roles'] if
                    pid in [ACL_FALLSKJERM_HI, ACL_FALLSKJERM_SU, ACL_FALLSKJERM_FSJ]) is True
                or app.globals['user_id'] in resource_acl[perm]['roles'] is True
        ):
            return True

    return has_permission(resource_acl, perm)


def after_fetched(response):
    """ Modify response after GETing an observation
    This hook checks if permission on each observation
    If closed, then it will anonymize each observation wo w or x rights
    """
    # Just to be sure, we remove all data if anything goes wrong!
    # response.set_data({})
    try:
        if isinstance(response, list):

            for key, val in enumerate(response):

                response[key]['acl_user'] = user_persmissions(response[key]['acl'], response[key]['workflow']['state'])

                if response[key]['workflow']['state'] == 'closed':

                    if not has_nanon_permission(response[key]['acl'], 'execute', 'closed'):
                        response[key]['acl_user'] = user_persmissions(response[key]['acl'], 'closed')
                        response[key] = anon.anonymize_ors(response[key])


        elif isinstance(response, dict):
            response['acl_user'] = user_persmissions(response['acl'], response['workflow']['state'])
            """For item return nanon if roles match hi in club or fs"""
            if response.get('workflow', False) and 'state' in response['workflow']:
                if response['workflow']['state'] == 'closed':
                    if not has_nanon_permission(response['acl'], 'execute', 'closed'):
                        response = anon.anonymize_ors(response)

            ### REMOVE
            if response.get('weather', False):

                if response['weather'].get('auto', False):

                    if response['weather']['auto'].get('taf', False):
                        try:
                            import pytaf
                            taf_raw = response['weather']['auto'].get('taf')
                            # print(taf_raw[17:])
                            taf = pytaf.TAF(taf_raw[17:])
                            decoder = pytaf.Decoder(taf)
                            response['weather']['auto'].update({'taf_decoded': decoder.decode_taf()})
                        except Exception as e:
                            app.logger.info("ERR TAF ", e)
                            pass

                    if response['weather']['auto'].get('metar', False):
                        try:
                            from metar import Metar
                            met = Metar.Metar("METAR %s" % response['weather']['auto']['metar'][17:])
                            response['weather']['auto'].update({'metar_decoded': met.string()})

                        except Exception as e:
                            app.logger.info("ERR Metar ", e)
                            pass

        response['acl'] = get_user_acl_mapping(response['acl'])
    # except Exception as e:
    #    print('########### ERR: ', e)
    except KeyError as e:
        app.logger.info("Keyerror in hook error: {}".format(e))
        eve_helper.eve_abort(500,
                             'Server experienced problems (keyerror) anonymousing the observation and aborted as a safety measure')
    except Exception as e:
        app.logger.info("Unexpected error: {}".format(e))
        eve_helper.eve_abort(500,
                             'Server experienced problems (unknown) anonymousing the observation and aborted as a safety measure')


@require_token()
def before_get(request, lookup):
    print('################')
    print('REQ', request)
    print('LOOKUP', lookup)
    lookup.update({'$or': [{"acl.read.roles": {'$in': app.globals['acl']['roles']}}, \
                           {"acl.read.users": {'$in': [app.globals.get('user_id')]}}]})


@require_token()
def before_patch(request, lookup):
    lookup.update({'$or': [{"acl.write.roles": {'$in': app.globals['acl']['roles']}}, \
                           {"acl.write.users": {'$in': [app.globals.get('user_id')]}}]})


@require_token()
def before_post_comments(resource, items):
    if resource == 'fallskjerm/observation/comments':
        items[0].update({'user': int(app.globals.get('user_id'))})
