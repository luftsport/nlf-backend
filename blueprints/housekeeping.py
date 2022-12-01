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
    ACTIVITIES
)
from datetime import datetime, timedelta, timezone
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
    message = 'Det ser ut til at det har gått {0} dager uten aktivitet for OBSREG #{1} "{2}". Dette er første purring.\r\n\r\n' \
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


def _do_second(obsreg, activity):
    message = 'Det ser ut til at det har gått {0} dager uten aktivitet for OBSREG #{1} "{2}". Dette er andre purring.\r\n\r\n' \
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


def get_observations(activity, cutoff):

    col = app.data.driver.db['{}_observations'.format(activity)]
    cursor = col.find(
        {
            '_updated': {'$lte': cutoff},
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


def filter_chores(l, _date):
    """Filter by known types and then verify that it is done AFTER last _update for obsreg!!"""
    n = [x for x in l if
         x['type'] in [HOUSEKEEPING_FIRST_CHORE, HOUSEKEEPING_SECOND_CHORE, HOUSEKEEPING_ACTION_CHORE] and x[
             '_created'] >= _date]
    return n


def check_first(l):
    try:
        before = datetime.now(timezone.utc) - timedelta(days=HOUSEKEEPING_FIRST_CHORE_DAYS_GRACE)
        if l[0]['type'] == HOUSEKEEPING_FIRST_CHORE and before >= l[0]['_created']:
            return True
    except Exception as e:
        pass

    return False


def check_second(l):
    try:
        before = datetime.now(timezone.utc) - timedelta(
            days=HOUSEKEEPING_SECOND_CHORE_DAYS_GRACE - HOUSEKEEPING_FIRST_CHORE_DAYS_GRACE)
        if l[0]['type'] == HOUSEKEEPING_SECOND_CHORE and before >= l[0]['_created']:
            return True
    except Exception as e:
        pass

    return False


def check_action(notifications):
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
        pass

    return False


def check_any(l) -> bool:
    """
    :param l: list of notifications
    :return: boolean has any
    """
    if len([x['type'] for x in l if
            x['type'] in [HOUSEKEEPING_FIRST_CHORE, HOUSEKEEPING_SECOND_CHORE]]) > 0:
        return True

    return False


def get_recepients(obsreg) -> list:
    try:
        return parse_acl_flat_by_permissions(obsreg.get('acl', {}), permissions=HOUSEKEEPING_ACL_RECIPIENTS)
    except:
        pass

    return []


@Housekeeping.route("/<string:activity>/<string:token>", methods=['POST'])
def housekeeping(activity, token):
    """
    """

    if token == HOUSEKEEPING_TOKEN and activity in ACTIVITIES:

        # Assign bot to user:
        # Set in app context
        g.user_id = HOUSEKEEPING_USER_ID

        msg = []

        # get all obsregs:
        cutoff = datetime.now(timezone.utc) - timedelta(days=HOUSEKEEPING_CHORE_DAYS_GRACE_MIN)
        status, obsregs = get_observations(activity, cutoff)

        if status is True:

            # iterate every obsreg:
            for obsreg in obsregs:
                #if obsreg['id'] != 652:
                #    continue
                # get all notifications for observation
                n_status, notifications = get_notifications(obsreg['_id'], activity)

                if n_status is True:

                    if check_any(notifications) is True:

                        # Har gjort andre warning
                        if check_second(filter_chores(notifications, obsreg['_updated'])) is True:

                            # Build message
                            msg.append(
                                {'id': obsreg['id'],
                                 'last_updated': obsreg['_updated'],
                                 'last_housekeeping': filter_chores(notifications, obsreg['_updated'])[0]['type'],
                                 'days_since_last_action': (datetime.now(timezone.utc) - obsreg['_updated']).days,
                                 'action': HOUSEKEEPING_ACTION_CHORE,
                                 'recipients': get_recepients(obsreg),
                                 'activity': activity,
                                 'event_from': f'{activity}_observations',
                                 'event_from_id': obsreg['_id']
                                 }
                            )

                            # Do action
                            _do_action(obsreg, activity)

                        # Har gjort første warning
                        elif check_first(filter_chores(notifications, obsreg['_updated'])) is True:
                            msg.append(
                                {'id': obsreg['id'],
                                 'last_updated': obsreg['_updated'],
                                 'last_housekeeping': filter_chores(notifications, obsreg['_updated'])[0]['type'],
                                 'days_since_last_action': (datetime.now(timezone.utc) - obsreg['_updated']).days,
                                 'action': HOUSEKEEPING_SECOND_CHORE,
                                 'recipients': get_recepients(obsreg),
                                 'activity': activity,
                                 'event_from': f'{activity}_observations',
                                 'event_from_id': obsreg['_id']
                                 }
                            )
                            _do_second(obsreg, activity)


                        # Got chores, but not old enough
                        else:
                            tmp_type = None
                            try:
                                tmp_type = filter_chores(notifications, obsreg['_updated'])[0]['type']
                            except:
                                pass

                            msg.append(
                                {'id': obsreg['id'],
                                 'last_updated': obsreg['_updated'],
                                 'last_housekeeping': tmp_type,
                                 'days_since_last_action': (datetime.now(timezone.utc) - obsreg['_updated']).days,
                                 'action': None,
                                 'recipients': [],
                                 'activity': activity,
                                 'event_from': f'{activity}_observations',
                                 'event_from_id': obsreg['_id']
                                 }
                            )

                    # Vi er over første warning uten noe har skjedd!!
                    else:
                        # Alle er uansett før dette!
                        if obsreg['_updated'] <= cutoff:
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
                # except Exception as e:
        try:
            response, _, _, return_code, location_header = post_internal('housekeeping', msg)
            print('[POST]', response, return_code)
        except Exception as e:
            print('[ERR housekeeping]', e)
        return eve_response(msg, 200)

    # @TODO refactor eve_* messages as eve_access_denied etc
    return eve_abort(403, 'Access denied')
