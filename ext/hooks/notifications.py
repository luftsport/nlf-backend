from flask import g, current_app as app
from ext.app.eve_helper import eve_abort
import json
from bson.objectid import ObjectId

from eve.methods.get import getitem_internal
from ext.auth.acl import has_permission


def before_get(request, lookup):
    """Make sure only recepient can read own messages"""
    lookup['recepient'] = g.user_id


def before_insert(items):
    for document in items:
        document['owner'] = g.user_id


def before_patch(request, lookup):
    lookup.update({'owner': g.user_id})


def before_delete(request, lookup):
    lookup.update({'owner': g.user_id})


def before_aggregation(endpoint, pipeline):
    """Before get or aggregation, check permissions
    If OBSREG is closed, none?"""

    if endpoint == 'notifications_events':
        _id = pipeline[0].get('$match', {}).get('event_from_id')

        resource = pipeline[0].get('$match', {}).get('event_from')
        item, _date, etag, status = getitem_internal(resource, **{'_id': _id})

        if (
                (item.get('workflow', {}).get('state', 'closed') == 'closed' and item.get('acl_user', {}).get('x',
                                                                                                              False) is False)
                or
                (item.get('acl_user', {}).get('r', False) is False)
        ):
            return eve_abort(403, 'No access')
