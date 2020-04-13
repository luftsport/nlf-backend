from flask import current_app as app
import ext.app.eve_helper as eve_helper
import json
from bson.objectid import ObjectId

from eve.methods.get import getitem_internal
from ext.auth.acl import has_permission


# from ext.app.decorators import require_token # Already authenticated

def before_insert(items):
    print('Before POST content to database')
    print(items)
    # payload = json.loads(response.get_data().decode('UTF-8'))
    for document in items:
        # update document 'userid' field according to my_arg
        # value. replace with custom logic.
        document['owner'] = app.globals.get('user_id')


def before_patch(request, lookup):
    lookup.update({'owner': app.globals.get('user_id')})


def before_delete(request, lookup):
    lookup.update({'owner': app.globals.get('user_id')})


def before_aggregation(endpoint, pipeline):
    """Before get or aggregation, check permissions
    If ORS is closed, none?"""

    if endpoint == 'notifications_events':
        print(endpoint, pipeline)

        _id = pipeline[0].get('$match', {}).get('event_from_id')
        resource = pipeline[0].get('$match', {}).get('event_from')
        item, _date, etag, status = getitem_internal(resource, **{'_id': _id})

        print(item.get('acl'))

        # ors? closed? Hwo has access??
        print('PERMISSIONS?', has_permission(item.get('acl'), 'read'))

        # print(status, response)
