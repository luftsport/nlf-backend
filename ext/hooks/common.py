from flask import g

def _set_owner(item):
    item['owner'] = g.user_id
    return item


def on_insert_set_owner(items):
    i = 0
    for item in items:
        items[i] = _set_owner(item)
        i += 1


def on_update_set_owner(updates, original):
    updates = _set_owner(updates)
