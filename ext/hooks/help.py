
from flask import current_app as app
import ext.app.eve_helper as eve_helper
import ext.auth.helpers as h
import json
from bson.objectid import ObjectId

helper = h.Helpers()

def on_insert_items(items):
    for item in items:
        on_insert_item(item)

def on_insert_item(item):
    #superadmin = helper.get_role_by_ref(ref='superadmin')
    if {'activity': 0, 'org': 0, 'role': 202639} in app.globals['acl']['roles']:
        #if superadmin in app.globals['acl']['roles']:
        item['owner'] = app.globals['user_id']
        item['acl'] = {'read': { 'activity' : 0, 'club' : 0, 'role' : 10000000 },
                       'write': {'user': [app.globals['user_id']]}}

    else:
        eve_helper.eve_abort(404, 'No access to this item')

def before_post(request, payload=None):

    print(request)
    print(payload)

    superadmin = helper.get_role_by_ref(ref='superadmin')

    if superadmin in app.globals['acl']['roles']:
        payload['owner'] = app.globals['user_id']

    else:
        eve_helper.eve_abort(404, 'No access to this item')

def after_post(request, response):

    try:
        payload = json.loads(response.get_data().decode('UTF-8'))
        print(payload)
    except:
        print('Error')
    if request.method == 'POST' and '_id' in payload and payload['_status'] == 'OK':
        superadmin = helper.get_role_by_ref(ref='superadmin')
        acl = {'write': {'user': [app.globals['user_id']]}}
        col = app.data.driver.db['help']
        col.update_one({'_id': ObjectId(payload.get('_id'))}, {"$set": {"acl": acl}})


def before_patch(request, lookup):
    print(request)
    print(app.globals['acl']['roles'])
    # lookup.update({"acl.write.users": {'$in': [app.globals.get('user_id')]}})
    """
    lookup.update({'$or': [{"acl.write.users": {'$in': [app.globals.get('user_id')]}},
                           {"acl.write.roles": {'$in': app.globals['acl']['roles']}}
                           ]
    })
    """


def before_delete(request, lookup):
    # lookup.update({"acl.write.users": {'$in': [app.globals.get('user_id')]}})
    """
    lookup.update({'$or': [{"acl.write.roles": {'$in': app.globals['acl']['roles']}},
                           {"acl.write.users": {'$in': [app.globals.get('user_id')]}}]
    })
    """

