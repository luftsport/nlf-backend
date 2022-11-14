"""

    Aircrafts hooks:
    ===============

"""

from ext.app.decorators import *

def on_insert(items):
    for key, item in enumerate(items):
        items[key]['updated_by'] = int(g.user_id)


def on_update(item, original):
    item['updated_by'] = int(g.user_id)
