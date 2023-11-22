"""

    Aircrafts hooks:
    ===============

"""

from ext.app.decorators import *
from flask import current_app as app, redirect, abort, Response
def on_insert(items):
    for key, item in enumerate(items):
        items[key]['updated_by'] = int(g.user_id)


def on_update(item, original):
    item['updated_by'] = int(g.user_id)

def after_GET(request, payload):
    print('##################################################->')
    #print('Dadada')
    headers = {
        'Location': '/ABRACADABRA'
    }
    abort(
        Response(
            response=None,
            status=301,
            headers=headers
        )
    )