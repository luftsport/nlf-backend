from flask import current_app as app


def _set_owner(item):
    item['owner'] = app.globals.get('user_id', None)
    return item


def on_insert_set_owner(items):
    i = 0
    for item in items:
        items[i] = _set_owner(item)
        i += 1


def on_update_set_owner(updates, original):
    updates = _set_owner(updates)
