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
    """Placeholder for after GET hook, to be able to test if this is working
    app.logger.debug('##################################################->')
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
    """
    pass
