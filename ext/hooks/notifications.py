from flask import g, current_app as app
from ext.app.eve_helper import eve_abort
import json
from bson.objectid import ObjectId

from eve.methods.get import getitem_internal
from ext.auth.acl import has_permission


def before_get(request, lookup):
    """Make sure only recepient can read own messages"""
    lookup['$or'] = [{'sender': g.user_id}, {'recepient': g.user_id}]


def before_insert(items):
    for document in items:
        document['owner'] = g.user_id


def before_patch(request, lookup):
    lookup.update({'owner': g.user_id})


def before_delete(request, lookup):
    lookup.update({'owner': g.user_id})


def before_aggregation(endpoint, pipeline):
    """Before get or aggregation
    """

    # Notifications
    # If OBSREG is closed, only see own notifications if not
    # @TODO make whitelist not blacklist
    if endpoint == 'notifications_events':
        # Only allow own notifications
        pipeline[0]['$match']['$or'] = [{'recepient': g.user_id}, {'sender': g.user_id}]  # Make sure to update when typo is fixed

        _id = pipeline[0].get('$match', {}).get('event_from_id')

        resource = pipeline[0].get('$match', {}).get('event_from')

        if resource in ['fallskjerm_observations', 'seilfly_observations', 'sportsfly_observations',
                        'motorfly_observations', 'modellfly_observations']:
            # Get observation - if user has access!
            item, _date, etag, status = getitem_internal(resource, **{'_id': _id})

            if (
                    status == 200  # there is an observation we can access
                    and
                    (
                            item.get('workflow', {}).get('state', 'closed') != 'closed'  # only if not closed
                            or
                            item.get('acl_user', {}).get('x', False) is True  # or if we have execute access
                            or
                            item.get('reporter', 0) == g.user_id  # or if user is reporter
                    )

            ):
                # Only now we can allow by removing filter
                pipeline[0]['$match'].pop('recepient', None)
                pipeline[0]['$match'].pop('recipient', None)  # Make sure if typo gets corrected
                # pipeline[0]['$match'].pop('sender', None)
