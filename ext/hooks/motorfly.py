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
from ext.hooks.motorfly_signals import signal_activity_log, \
    signal_change_owner  # signal_init_acl signal_insert_workflow,
from ext.hooks.motorfly_signals import signal_g_init_acl, signal_motorfly_insert_workflow

from ext.scf import ACL_MOTORFLY_SKOLESJEF, ACL_MOTORFLY_ORS, ACL_MOTORFLY_DTO
from ext.workflows.motorfly_observations import ObservationWorkflow, get_wf_init, get_acl_init
from ext.app.seq import increment
from ext.app.lungo import get_person_from_role
from datetime import datetime


def ors_before_insert(items):
    for item in items:
        ors_before_insert_item(item)


def ors_before_insert_item(item):
    """Do everything needed before processing
    Add WF
    Add other known...
    """
    try:
        if 'discipline' in item and item.get('discipline', 0) > 0:

            ors_id = increment('ors_motorfly')

            if ors_id:
                item['id'] = ors_id
            else:
                eve_abort(422, 'Could not create ORS, missing increment')

            item['when'] = datetime.utcnow()
            item['reporter'] = app.globals.get('user_id')
            item['owner'] = app.globals.get('user_id')
            item['watchers'] = [app.globals.get('user_id')]
            item['workflow'] = get_wf_init(app.globals.get('user_id'))

            item['organization'] = {}
            _, _person_ors = get_person_from_role(ACL_MOTORFLY_ORS)
            item['organization']['ors'] = _person_ors

            persons_dto = ACL_MOTORFLY_DTO.copy()
            persons_dto['org'] = item.get('discipline')
            _, _persons_dto = get_person_from_role(persons_dto)
            item['organization']['dto'] = _persons_dto

            item['acl'] = get_acl_init(app.globals.get('user_id'), item.get('discipline'))


    except Exception as e:
        print('Error', e)
        eve_abort(422, 'Could not create ORS')


def ors_after_insert(items):
    for item in items:
        ors_after_insert_item(item)


def ors_after_insert_item(item):
    wf = ObservationWorkflow(object_id=item.get('_id', ''), user_id=app.globals.get('user_id'))
    if wf.get_current_state().get('state', '') == 'draft':
        wf.notify_created()

    """   
    try:
        wf = ObservationWorkflow(object_id=item.get('_id', ''), user_id=app.globals.get('user_id'))
        
        if wf.get_current_state() == 'draft':
            wf.notify_created()
    
    except Exception as e:
        print('ERR item {}'.format(item))
        print('ERR cant process WF: {}'.format(e))
        pass

    """


def after_g_post(request, response):
    payload = json.loads(response.get_data().decode('UTF-8'))

    signal_motorfly_insert_workflow.send({'app': app, 'payload': payload})

    signal_g_init_acl.send({'app': app, 'payload': payload})


@require_token()
def before_post(request, payload=None):
    pass


def after_patch(request, response):
    """ Change owner, owner is readonly
    """
    signal_change_owner.send(app, response=response)


def after_fetched_p(response, _id):
    # print('##### RESPONSE ####')
    # print(response)
    pass


def after_fetched_diffs(response):
    # print('########', response)
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
                    pid in [ACL_MOTORFLY_SKOLESJEF, ACL_MOTORFLY_ORS]) is True
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
    if isinstance(response, dict):
        response['acl_user'] = get_user_acl_mapping(response.get('acl', {}))
        print('ORS state', response.get('workflow', {}).get('state', 'NONE'))
        print('ACL', response.get('acl', 'NONE'))
    try:
        if isinstance(response, list):

            for key, val in enumerate(response):

                # response[key]['acl_user'] = user_persmissions(response[key]['acl'], response[key]['workflow']['state'])
                response[key]['acl_user'] = get_user_acl_mapping(response[key]['acl'])

                if response[key]['workflow']['state'] == 'closed':

                    if not has_nanon_permission(response[key]['acl'], 'execute', 'closed'):
                        # response[key]['acl_user'] = user_persmissions(response[key]['acl'], 'closed')
                        response[key] = anon.anonymize_ors(response[key])


        elif isinstance(response, dict):
            # response['acl_user'] = user_persmissions(response['acl'], response['workflow']['state'])

            response['acl_user'] = get_user_acl_mapping(response['acl'])

            """For item return nanon if roles match hi in club or fs"""
            if response.get('workflow', False) and 'state' in response['workflow']:
                if response['workflow']['state'] == 'closed':
                    if not has_nanon_permission(response['acl'], 'execute', 'closed'):
                        response = anon.anonymize_ors(response)


    # except Exception as e:
    #    print('########### ERR: ', e)
    except KeyError as e:
        app.logger.info("Keyerror in hook error: {}".format(e))
        eve_helper.eve_abort(500,
                             'Server experienced problems (keyerror) anonymousing the observation and aborted as a safety measure')
    except Exception as e:
        app.logger.info("Unexpected error: {}".format(e))
        eve_helper.eve_abort(500,
                             'Server experienced problems (unknown) anonymousing the observation and aborted as a safety measure {}'.format(
                                 e))


def before_get_todo(request, lookup):
    lookup.update({'$and': [{'workflow.state': {'$nin': ['closed', 'withdrawn']}},
                            {'$or': [{'acl.execute.users': {'$in': [app.globals['user_id']]}},
                                     {'acl.execute.roles': {'$in': app.globals['acl']['roles']}}]}]})


@require_token()
def before_get(request, lookup):
    # print('################')
    # print('REQ', request)
    # print('LOOKUP', lookup)
    lookup.update({'$or': [{"acl.read.roles": {'$in': app.globals['acl']['roles']}},
                           {"acl.read.users": {'$in': [app.globals.get('user_id')]}}]})


@require_token()
def before_patch(request, lookup):
    lookup.update({'$or': [{"acl.write.roles": {'$in': app.globals['acl']['roles']}},
                           {"acl.write.users": {'$in': [app.globals.get('user_id')]}}]})


@require_token()
def before_post_comments(resource, items):
    if resource == 'fallskjerm/observation/comments':
        items[0].update({'user': int(app.globals.get('user_id'))})
