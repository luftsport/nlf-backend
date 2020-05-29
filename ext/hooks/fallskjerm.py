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
import ext.app.eve_helper as eve_helper
from ext.app.decorators import *

from ext.scf import ACL_FALLSKJERM_HI, ACL_FALLSKJERM_SU_GROUP_LIST, ACL_FALLSKJERM_FSJ
from ext.workflows.fallskjerm_observations import ObservationWorkflow, get_wf_init, get_acl_init
from ext.app.seq import increment
from ext.app.lungo import get_person_from_role
from datetime import datetime
from ext.app.notifications import ors_save, ors_workflow, broadcast


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
                eve_abort(422, 'Could not create ORS, missing increment')

            item['when'] = datetime.utcnow()
            item['reporter'] = app.globals.get('user_id')
            item['owner'] = app.globals.get('user_id')
            item['watchers'] = [app.globals.get('user_id')]
            item['workflow'] = get_wf_init(app.globals.get('user_id'))

            role_hi = ACL_FALLSKJERM_HI.copy()
            role_hi['org'] = item.get('discipline')
            _, hi = get_person_from_role(role_hi)
            item['organization'] = {'hi': hi}

            item['acl'] = get_acl_init(app.globals.get('user_id'), item['discipline'])

    except Exception as e:
        eve_abort(422, 'Could not create ORS')
        pass


def ors_after_inserted(items):
    for item in items:
        ors_after_inserted_item(item)


def ors_after_inserted_item(item):
    wf = ObservationWorkflow(object_id=item.get('_id', ''), user_id=app.globals.get('user_id'))
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
                    org=response.get('discipline', 0)
                        is False):
                for index, val in enumerate(response):
                    response[index] = anon.anonymize_ors(response[index])
    else:
        ors_after_fetched(response)


def ors_after_fetched(response):
    """ Modify response after GETing an observation
    This hook checks if permission on each observation
    If closed, then it will anonymize each observation wo w or x rights
    """
    # Just to be sure, we remove all data if anything goes wrong!
    # response.set_data({})
    if isinstance(response, dict):
        response['acl_user'] = get_user_acl_mapping(response.get('acl', {}))

    try:
        if isinstance(response, list):

            for key, val in enumerate(response):

                # response[key]['acl_user'] = user_persmissions(response[key]['acl'], response[key]['workflow']['state'])
                response[key]['acl_user'] = get_user_acl_mapping(response[key]['acl'])

                if response[key]['workflow']['state'] == 'closed':

                    if has_nanon_permission(
                            resource_acl=response[key].get('acl', []),
                            perm='execute',
                            state='closed',
                            model='fallskjerm',
                            org=response[key].get('discipline', 0)
                            is False):
                        # response[key]['acl_user'] = user_persmissions(response[key]['acl'], 'closed')
                        response[key] = anon.anonymize_ors(response[key])


        elif isinstance(response, dict):
            # response['acl_user'] = user_persmissions(response['acl'], response['workflow']['state'])

            # SocketIO
            broadcast('Somebody is looking at ORS#{}'.format(response['id']))

            response['acl_user'] = get_user_acl_mapping(response['acl'])

            """For item return nanon if roles match hi in club or fs"""
            if response.get('workflow', False) and 'state' in response['workflow']:
                if response['workflow']['state'] == 'closed':
                    if has_nanon_permission(
                            resource_acl=response[0].get('acl', []),
                            perm='execute',
                            state='closed',
                            model='fallskjerm',
                            org=response.get('discipline', 0)
                            is False):
                        response = anon.anonymize_ors(response)

    except KeyError as e:
        app.logger.info("Keyerror in hook error: {}".format(e))
        eve_helper.eve_abort(500,
                             'Server experienced problems (keyerror) anonymousing the observation and aborted as a safety measure')
    except Exception as e:
        app.logger.info("Unexpected error: {}".format(e))
        eve_helper.eve_abort(500,
                             'Server experienced problems (unknown) anonymousing the observation and aborted as a safety measure')


@require_token()
def ors_before_get_todo(request, lookup):
    lookup.update({'$and': [{'workflow.state': {'$nin': ['closed', 'withdrawn']}},
                            {'$or': [{'acl.execute.users': {'$in': [app.globals['user_id']]}},
                                     {'acl.execute.roles': {'$in': app.globals['acl']['roles']}}]}]})


@require_token()
def ors_before_get(request, lookup):
    lookup.update({'$or': [{"acl.read.roles": {'$in': app.globals['acl']['roles']}},
                           {"acl.read.users": {'$in': [app.globals.get('user_id')]}}]})


@require_token()
def ors_before_patch(request, lookup):
    lookup.update({'$or': [{"acl.write.roles": {'$in': app.globals['acl']['roles']}},
                           {"acl.write.users": {'$in': [app.globals.get('user_id')]}}]})


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
        items[0].update({'user': int(app.globals.get('user_id'))})
