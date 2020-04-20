"""
    Observation Workflow Controller
    ===============================

    Model: ext.workflows.observation.ObservationWorkflow

    @todo: Signals on change signal to communications to dispatch an update to the watchers
           http://stackoverflow.com/questions/16163139/catch-signals-in-flask-blueprint

"""
from flask import Blueprint, current_app as app  # , Response, abort, jsonify, make_response
import datetime

# Notification
from ext.app.notifications import strip_tags, REMINDER_DELTA

# Need custom decorators
from ext.app.decorators import *
from ext.app.eve_helper import eve_response, eve_response_pppd
from eve.methods.get import get_internal
from ext.auth.acl import get_acl, parse_acl_flat
from ext.app.notifications import ors_message, ors_reminder

Notifications = Blueprint('Notifications', __name__, )


@Notifications.route("/message", methods=['POST'])
@require_token()
def message():
    try:

        # ARGS
        args = request.get_json(force=True)  # use force=True to do anyway!
        event_from = args.get('event_from', None)
        event_from_id = args.get('event_from_id', None)
        msg = strip_tags(args.get('message', None))

        if event_from is None or event_from_id is None or msg is None:
            eve_abort(422, 'Missing parameters')

        # Can't do if closed or withdrawn
        status, acl, rest = get_acl(event_from, event_from_id, projection={'acl': 1, 'workflow.state': 1, 'id': 1, 'discipline': 1, 'tags': 1})

        if rest.get('workflow', {}).get('state', 'closed') in ['closed', 'withdrawn']:
            return eve_response_pppd(
                {'data': 'Observasjonen er {}'.format(rest.get('workflow', {}).get('state', 'closed'))},
                403,
                'Observation is {}'.format(rest.get('workflow', {}).get('state', 'closed'))
            )

        k = parse_acl_flat(acl)
        # If not self too
        recepients = [x for x in k if x != app.globals.get('user_id', None)]
        ors_message(recepients=recepients, event_from=event_from, event_from_id=event_from_id, message=msg, ors_id=rest.get('id', None), org_id=rest.get('discipline', None), ors_tags=rest.get('tags', []))

        return eve_response(recepients, 200)

    except Exception as e:
        app.logger.exception('Error creating message for observation')
        return eve_response({}, 500)


# @Notifications.route("/reminder/<string:app>/<string:activity>/<objectid:_id>", methods=['POST'])
# def notify(app, activity, _id):
@Notifications.route("/reminder", methods=['POST'])
@require_token()
def reminder():
    """  """

    """
    1) Check if has access and if not X
    2) Find the x'es 
    3) make sure sender not an x!! see 1...
    4) make sure we're not trying to notify too soon after last one => get last notification for this x+event_from+event_from_id
    5) find x'es user settings - says something about their transmission preferences (mail, aggregate, sms...)
    6) Notify x'es! or both x and w - with users preferences!
    """
    try:
        # Args
        args = request.get_json(force=True)  # use force=True to do anyway!
        event_from = args.get('event_from', None)
        event_from_id = args.get('event_from_id', None)

        if event_from is None or event_from_id is None:
            return eve_response_pppd({}, 403, 'Observation is closed')

        if event_from is None or event_from_id is None or message is None:
            eve_abort(422, 'Missing parameters')

        status, acl, rest = get_acl(event_from, event_from_id, projection={'acl': 1, 'workflow.state': 1, 'id': 1, 'discipline': 1, 'tags': 1})
        print('ACLS', acl)
        if rest.get('workflow', {}).get('state', 'closed') in ['closed', 'withdrawn']:
            return eve_response_pppd(
                {'data': 'Observasjonen er {}'.format(rest.get('workflow', {}).get('state', 'closed'))},
                403,
                'Observation is {}'.format(rest.get('workflow', {}).get('state', 'closed'))
            )

        recepients = parse_acl_flat(acl)
        disapproved_users = get_within_delay(event_from_id, 'ors_reminder', recepients) if len(recepients) > 0 else []

        # Check if same users
        # @TODO investigate if should be each user
        recepients.sort()
        disapproved_users.sort()
        if disapproved_users == recepients:
            return eve_response_pppd({'data': 'Please wait for the remaining graceperiod until {}'.format(
                (datetime.datetime.utcnow() - datetime.timedelta(seconds=REMINDER_DELTA))
            )
            },
                429,
                'Too soon to send notification')

        # Remove disapproved
        recepients = [x for x in recepients if x not in disapproved_users and x != app.globals.get('user_id', None)]
        if len(recepients) == 0:
            return eve_response_pppd({'data': 'Fant ingen å sende til'}, 404, 'Found no recepients!')

        # Create notification
        ors_reminder(recepients, event_from=event_from, event_from_id=event_from_id, ors_id=rest.get('id', None), org_id=rest.get('discipline', None), ors_tags=rest.get('tags', []))
        return eve_response(recepients, 200)

    except Exception as e:
        app.logger.exception('Error creating reminder for observation')
        return eve_response({}, 500)


def get_within_delay(_id, event_type='ors_reminder', persons=[]):
    lookup = {
        'event_from_id': _id,
        'recepient': {'$in': persons},
        'type': event_type,
        'event_created': {'$gte': datetime.datetime.utcnow() - datetime.timedelta(seconds=REMINDER_DELTA)}
    }
    response, _, _, status, _ = get_internal('notifications', **lookup)
    return list(set([notification['recepient'] for notification in response['_items']]))
