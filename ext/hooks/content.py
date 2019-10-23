
from flask import current_app as app
import ext.app.eve_helper as eve_helper
import json
from bson.objectid import ObjectId

"""

on_insert_<resource_name>
def event(items)


on_inserted_<resource_name>
def event(items)

PATCH / UPDATE
on_update_<resource_name>
def event(updates, original)

on_updated_<resource_name>
def event(updates, original)

# BEFORE
app.on_pre_GET_contacts += pre_contacts_get_callback

app.on_pre_GET_<resource> = on_before (request, lookup)




"""
def before_insert(items):
    # print('Before POST content to database')
    # print(items)
    # payload = json.loads(response.get_data().decode('UTF-8'))
    for document in items:
        # update document 'userid' field according to my_arg
        # value. replace with custom logic.
        document['owner'] = app.globals.get('user_id')

def before_patch(request, lookup):
    #print('Before PATCH content')
    #print(request)
    #print(lookup)
    pass
    
def before_delete(request, lookup):
    lookup.update({'owner': app.globals.get('user_id')}, response=resp)
