"""
    Observation Housekeeping
    ========================

    @TODO write a file lock by activity to avoid race conditions or use app.globals?
"""
from flask import g, Blueprint, current_app as app, request, Response, abort, jsonify, make_response
from eve.methods.post import post_internal
import base64
# from ext.workflows.fallskjerm_observations import ObservationWorkflow

# Need custom decorators
from ext.app.decorators import *
from ext.app.eve_helper import eve_response
from ext.app.notifications import ors_housekeeping

# @TODO refactor settings to a dict opening possibility for different settings between activities
from ext.scf import (
    HOUSEKEEPING_USER_TOKEN,
    HOUSEKEEPING_USER_ID,
    HOUSEKEEPING_FIRST_CHORE,
    HOUSEKEEPING_FIRST_CHORE_DAYS_GRACE,
    HOUSEKEEPING_SECOND_CHORE,
    HOUSEKEEPING_SECOND_CHORE_DAYS_GRACE,
    HOUSEKEEPING_ACTION_CHORE,
    HOUSEKEEPING_ACTION_CHORE_DAYS_GRACE,
    HOUSEKEEPING_CHORE_DAYS_GRACE_MIN,
    HOUSEKEEPING_TOKEN,
    HOUSEKEEPING_ACL_RECIPIENTS,
    HOUSEKEEPING_ANY_CHORE_BEFORE,
    HOUSEKEEPING,
    ACTIVITIES
)
from datetime import datetime, timedelta, timezone
import pytz
from ext.auth.acl import parse_acl_flat_by_permissions
from ext.auth.tokenauth import TokenAuth

# @TODO refactor after workflow refactoring
from ext.workflows.fallskjerm_observations import WF_FALLSKJERM_TRANSITIONS, WF_FALLSKJERM_TRANSITIONS_ATTR, \
    ObservationWorkflow as wf_fallskjerm
from ext.workflows.motorfly_observations import WF_MOTORFLY_TRANSITIONS, WF_MOTORFLY_TRANSITIONS_ATTR, \
    ObservationWorkflow as wf_motorfly
from ext.workflows.seilfly_observations import WF_SEILFLY_TRANSITIONS, WF_SEILFLY_TRANSITIONS_ATTR, \
    ObservationWorkflow as wf_seilfly
from ext.workflows.sportsfly_observations import WF_SPORTSFLY_TRANSITIONS, WF_SPORTSFLY_TRANSITIONS_ATTR, \
    ObservationWorkflow as wf_sportsfly

Housekeeping = Blueprint('Housekeeping', __name__, )

HOUSEKEEPING_FOOTER = 'Dette er en automatisk generert purring etter følgende tidsfrister:\r\n' \
                      '- første purring skjer etter {0} dager med inaktivitet\r\n' \
                      '- andre purring skjer etter {1} dager med inaktivitet\r\n' \
                      '- etter {2} dager med inaktivitet sendes observasjonen automatisk tilbake eller den blir trukket tilbake.\r\n' \
                      '\r\n' \
                      '' \
    .format(HOUSEKEEPING_FIRST_CHORE_DAYS_GRACE,
            HOUSEKEEPING_SECOND_CHORE_DAYS_GRACE,
            HOUSEKEEPING_ACTION_CHORE_DAYS_GRACE,
            )


def _do_first(obsreg, activity):
    message = 'Det ser ut til at det har gått over {0} dager uten aktivitet for OBSREG #{1} {2}. Dette er første purring.\r\n\r\n' \
              'Fint om du tar tak i den så snart det lar seg gjøre.\r\n\r\n' \
              '{3}' \
        .format(HOUSEKEEPING_FIRST_CHORE_DAYS_GRACE, obsreg['id'], '/'.join(obsreg.get('tags', [])),
                HOUSEKEEPING_FOOTER)
    r = ors_housekeeping(recipients=get_recepients(obsreg),
                         event_type=HOUSEKEEPING_FIRST_CHORE,
                         event_from='{}_observations'.format(activity),
                         event_from_id=obsreg['_id'],
                         message=message,
                         ors_id=obsreg['id'],
                         org_id=obsreg['discipline'],
                         ors_tags=obsreg.get('tags', []))

    print('DO FIRST', r)


def _do_second(obsreg, activity):
    message = 'Det ser ut til at det har gått over {0} dager uten aktivitet for OBSREG #{1} "{2}". Dette er andre purring.\r\n\r\n' \
              'Fint om du tar tak i den så snart det lar seg gjøre \r\n\r\n' \
              '{3}' \
        .format(HOUSEKEEPING_SECOND_CHORE_DAYS_GRACE, obsreg['id'], '/'.join(obsreg.get('tags', [])),
                HOUSEKEEPING_FOOTER)
    ors_housekeeping(recipients=get_recepients(obsreg),
                     event_type=HOUSEKEEPING_SECOND_CHORE,
                     event_from='{}_observations'.format(activity),
                     event_from_id=obsreg['_id'],
                     message=message,
                     ors_id=obsreg['id'],
                     org_id=obsreg['discipline'],
                     ors_tags=obsreg.get('tags', []))


def _do_action(obsreg, activity):
    # Do transition
    # @TODO refacoring workflows this should also be refactored
    action = None
    wf_activity = None
    if activity == 'motorfly':
        wf_activity = wf_motorfly
        transitions = WF_MOTORFLY_TRANSITIONS
        transitions_attr = WF_MOTORFLY_TRANSITIONS_ATTR
    elif activity == 'sportsfly':
        wf_activity = wf_sportsfly
        transitions = WF_SPORTSFLY_TRANSITIONS
        transitions_attr = WF_SPORTSFLY_TRANSITIONS_ATTR
    elif activity == 'seilfly':
        wf_activity = wf_seilfly
        transitions = WF_SEILFLY_TRANSITIONS
        transitions_attr = WF_SEILFLY_TRANSITIONS_ATTR
    elif activity == 'fallskjerm':
        wf_activity = wf_fallskjerm
        transitions = WF_FALLSKJERM_TRANSITIONS
        transitions_attr = WF_FALLSKJERM_TRANSITIONS_ATTR

    if wf_activity:

        # current state:
        curr_state = obsreg['workflow']['audit'][0].get('d', None)
        # previous state
        prev_state = obsreg['workflow']['audit'][0].get('s', None)

        # Only draft - withdraw!
        if curr_state == 'draft' and prev_state is None:
            action = 'withdraw'
            verb = 'trukket'
        else:
            # Sent back
            verb = 'sendt'
            # list of possible transitions
            l = [x for x in transitions if x['source'] == curr_state and x['dest'] == prev_state]
            if len(l) > 1:
                # Only reject
                l = [x for x in l if 'reject' in x['trigger']]

            if len(l) == 1:
                action = transitions_attr[l[0]['trigger']]['resource']

        if action is not None:
            comment = 'Observasjonen har vært inaktiv i over {} dager og er derfor automatisk {} tilbake' \
                .format(HOUSEKEEPING_ACTION_CHORE_DAYS_GRACE, verb)

            # Init correct
            wf = wf_activity(object_id=obsreg['_id'],
                             user_id=1,
                             comment=comment)

            # Now just do a transition
            if wf.get_resource_mapping().get(action, False):
                result = eval('wf.' + wf.get_resource_mapping().get(action) + '()')


def get_observations(activity, cutoff_date):
    col = app.data.driver.db['{}_observations'.format(activity)]
    cursor = col.find(
        {
            '_updated': {'$lte': cutoff_date},
            'workflow.state': {'$nin': ['withdrawn', 'closed']}
        },
        {
            'workflow': 1,
            'id': 1,
            'tags': 1,
            '_created': 1,
            '_updated': 1,
            'discipline': 1,
            'acl': 1
        }
    )
    _items = list(cursor.sort('_updated', 1))

    return True, _items


def get_notifications(_id, activity):
    event_from = '{}_observations'.format(activity)
    col = app.data.driver.db['notifications']
    cursor = col.find(
        {
            'event_from': event_from,
            'event_from_id': _id,
            # 'event_type': {'$in': ["housekeeping_obsreg_first_warning", "housekeeping_obsreg_second_warning"]},
        }
    )
    _items = list(cursor.sort('_created', -1))
    return True, _items


def filter_chores(notifications, _date):
    """Filter by known types and then verify that it is done AFTER last _update for obsreg!!"""
    try:
        return [
            x for x in notifications if
            x['type'] in [HOUSEKEEPING_FIRST_CHORE, HOUSEKEEPING_SECOND_CHORE, HOUSEKEEPING_ACTION_CHORE]
            and x['_created'] >= _date
        ]
    except Exception as e:
        app.logger.exception('Could not filter notifications')

    return []


def check_first(l):
    if len(l) > 0:
        try:
            before = datetime.now(timezone.utc) - timedelta(days=HOUSEKEEPING_FIRST_CHORE_DAYS_GRACE)
            if l[0]['type'] == HOUSEKEEPING_FIRST_CHORE and before >= l[0]['_created']:
                return True
        except Exception as e:
            app.logger.exception(f'Error checking for {HOUSEKEEPING_FIRST_CHORE}')

    return False


def check_second(l):
    if len(l) > 0:
        try:
            before = datetime.now(timezone.utc) - timedelta(
                days=HOUSEKEEPING_SECOND_CHORE_DAYS_GRACE - HOUSEKEEPING_FIRST_CHORE_DAYS_GRACE)
            if l[0]['type'] == HOUSEKEEPING_SECOND_CHORE and before >= l[0]['_created']:
                return True
        except Exception as e:
            app.logger.exception(f'Error checking for {HOUSEKEEPING_SECOND_CHORE}')

    return False


def check_action(notifications):
    if len(notifications) > 0:
        try:
            before = datetime.now(timezone.utc) - timedelta(days=HOUSEKEEPING_ACTION_CHORE_DAYS_GRACE)
            # if l[0]['type'] == HOUSEKEEPING_ACTION_CHORE and before >= l[0]['_created']:
            if (
                    notifications[0]['type'] == 'ors_workflow'
                    and notifications[0]['sender'] == 1
                    and notifications[0]['data']['action'] == 'reject'
                    and before >= notifications[0]['_created']
            ):
                return True
        except Exception as e:
            app.logger.exception(f'Error checking for {HOUSEKEEPING_ACTION_CHORE}')

    return False


def check_any(l) -> bool:
    """
    :param l: list of notifications
    :return: boolean has any
    """
    try:
        if len([x['type'] for x in l if
                x['type'] in [HOUSEKEEPING_FIRST_CHORE, HOUSEKEEPING_SECOND_CHORE]]) > 0:
            return True
    except Exception as e:
        app.logger.exception('Could not check for any chores')

    return False


def get_recepients(obsreg) -> list:
    try:
        r = parse_acl_flat_by_permissions(obsreg.get('acl', {}), permissions=HOUSEKEEPING_ACL_RECIPIENTS)
        app.logger.info('{}:Got following recepients {}'.format(obsreg['id'], r))

        # Make sure we have one recipient at least to make a notification!
        # There can be functions->person that do not exist anymore since organization is no longer active in NIF
        if len(r) == 0:
            r = [HOUSEKEEPING_USER_ID]
        return r
    except:
        app.logger.exception('Error parsing acl to flat permissions for housekeeping, failed OBSREG ID {}'.format(
            obsreg.get('id', None)))

    return []


@Housekeeping.route("/<string:activity>/<string:token>", methods=['POST'])
def housekeeping(activity, token):
    """
    @TODO get_recipients is called twice for each both msg for audit log and in _do_*
    """

    if HOUSEKEEPING is True and token == HOUSEKEEPING_TOKEN and activity in ACTIVITIES:

        # Assign bot to user:
        g.user_id = HOUSEKEEPING_USER_ID

        msg = []

        # Set cutoff date
        cutoff_date = pytz.utc.localize(datetime.utcnow()) - timedelta(days=HOUSEKEEPING_CHORE_DAYS_GRACE_MIN)
        # get all obsregs:
        status, obsregs = get_observations(activity, cutoff_date)

        if status is True:

            # iterate every obsreg:
            for obsreg in obsregs:
                # if obsreg['id'] != 652:
                #    continue

                # catchall for each
                try:
                    # get all notifications for observation
                    n_status, notifications = get_notifications(obsreg['_id'], activity)

                    if n_status is True:

                        # Check if anything is done over all notifications
                        if check_any(notifications) is True:

                            # Filter chores - chores after obsreg last updated:
                            filtered_chores = filter_chores(notifications, obsreg['_updated'])

                            # There is chores within cutoff
                            # Make sure we do the right chore next
                            if len(filtered_chores) > 0:

                                # Has second warning since obsreg last _updated?
                                if check_second(filtered_chores) is True:

                                    # Build message
                                    msg.append(
                                        {'id': obsreg['id'],
                                         'last_updated': obsreg['_updated'],
                                         'last_housekeeping': filter_chores(notifications, obsreg['_updated'])[0][
                                             'type'],
                                         'days_since_last_action': (
                                                 pytz.utc.localize(datetime.utcnow()) - obsreg['_updated']).days,
                                         'action': HOUSEKEEPING_ACTION_CHORE,
                                         'recipients': get_recepients(obsreg),
                                         'activity': activity,
                                         'event_from': f'{activity}_observations',
                                         'event_from_id': obsreg['_id']
                                         }
                                    )

                                    # Do workflow action
                                    _do_action(obsreg, activity)

                                # Has first warning since obsreg last _updated
                                elif check_first(filter_chores(notifications, obsreg['_updated'])) is True:
                                    msg.append(
                                        {'id': obsreg['id'],
                                         'last_updated': obsreg['_updated'],
                                         'last_housekeeping': filter_chores(notifications, obsreg['_updated'])[0][
                                             'type'],
                                         'days_since_last_action': (
                                                 pytz.utc.localize(datetime.utcnow()) - obsreg['_updated']).days,
                                         'action': HOUSEKEEPING_SECOND_CHORE,
                                         'recipients': get_recepients(obsreg),
                                         'activity': activity,
                                         'event_from': f'{activity}_observations',
                                         'event_from_id': obsreg['_id']
                                         }
                                    )
                                    _do_second(obsreg, activity)


                                # Got chores, but not old enough
                                # Could it be broken data?
                                else:
                                    tmp_type = None
                                    try:
                                        tmp_type = filter_chores(notifications, obsreg['_updated'])[0]['type']
                                    except:
                                        pass

                                    if tmp_type is not None:
                                        pass

                                    msg.append(
                                        {'id': obsreg['id'],
                                         'last_updated': obsreg['_updated'],
                                         'last_housekeeping': tmp_type,
                                         'days_since_last_action': (
                                                 datetime.now(timezone.utc) - obsreg['_updated']).days,
                                         'action': None,
                                         'recipients': [],
                                         'activity': activity,
                                         'event_from': f'{activity}_observations',
                                         'event_from_id': obsreg['_id']
                                         }
                                    )

                            # Check if chores but no chores since last update
                            else:
                                # Chores,  but no chores in grace period
                                # => It's been activity after last chore
                                # => send first warning

                                _do_first(obsreg, activity)

                                msg.append({
                                    'id': obsreg['id'],
                                    'last_updated': obsreg['_updated'],
                                    # Do not verify which chore we start all over again anyway
                                    'last_housekeeping': HOUSEKEEPING_ANY_CHORE_BEFORE,
                                    'days_since_last_action': (
                                            pytz.utc.localize(datetime.utcnow()) - obsreg['_updated']).days,
                                    'action': HOUSEKEEPING_FIRST_CHORE,
                                    'recipients': get_recepients(obsreg),
                                    'activity': activity,
                                    'event_from': f'{activity}_observations',
                                    'event_from_id': obsreg['_id']
                                })

                                """
                                # If one should start from last chore
                                # Filter from start of time
                                # filtered_chores_all_time = filter_chores(notifications, datetime(1970, 1, 1, 0, 0))
                                # Chores has been done
                                if len(filtered_chores_all_time) > 0:
                                # Make sure chores are before or eq last updated
                                # if filtered_chores_all_time[0]['_created'] <= obsreg['_updated']:
                                """

                        # No housekeeping registered at all
                        # _updated beyond grace for first warning => do first warning
                        else:
                            # Unnecessary comparison but to be sure
                            if obsreg['_updated'] <= cutoff_date:
                                msg.append(
                                    {'id': obsreg['id'],
                                     'last_updated': obsreg['_updated'],
                                     'last_housekeeping': None,
                                     'days_since_last_action': (datetime.now(timezone.utc) - obsreg['_updated']).days,
                                     'action': HOUSEKEEPING_FIRST_CHORE,
                                     'recipients': get_recepients(obsreg),
                                     'activity': activity,
                                     'event_from': f'{activity}_observations',
                                     'event_from_id': obsreg['_id']
                                     }
                                )
                                _do_first(obsreg, activity)

                except Exception as e:
                    app.logger('Error looping {} obsregs for housekeeping. Failed ID: {}'.format(
                        activity,
                        obsreg.get('id', None)
                    )
                    )
        try:
            response, _, _, return_code, location_header = post_internal('housekeeping', msg)
        except Exception as e:
            app.logger.exception(f'Error saving obsreg housekeeping audit log for {activity}')

        # always return a 200
        return eve_response(msg, 200)

    elif HOUSEKEEPING is False:
        return eve_abort(503, 'No housekeeping enabled')

    # @TODO refactor eve_* messages as eve_access_denied etc
    return eve_abort(403, 'Access denied')
