from flask import g, current_app as app


def _set_owner(item):
    item['owner'] = g.get('user_id', None)
    return item


def on_insert_set_owner(items):
    i = 0
    for item in items:
        items[i] = _set_owner(item)
        i += 1


def on_update_set_owner(updates, original):
    updates = _set_owner(updates)


def cast_choices(_item, wc=None):
    def _splitit(txt):
        x = txt.split('.')
        x = x[len(x) - 1]
        x = x[0].lower() + x[1:]
        return x

    def _get_attributes_with_choices():
        try:
            col = app.data.driver.db['e5x_attributes']
            with_choices = col.find({'choices_key': {'$ne': None}}, {'choices_key': 1, '_id': 0})
            return list(set([_splitit(x['choices_key']) for x in with_choices]))
        except:
            pass

        return []

    if wc is None:
        wc = _get_attributes_with_choices()

    if isinstance(_item, list) or isinstance(_item, dict):
        for k, v in _item.copy().items():
            if k in wc and isinstance(_item, dict):
                try:
                    if _item[k].get('value', None) is not None:
                        _item[k]['value'] = int(float(_item[k]['value']))
                except:
                    # Just let it pass, it might be wrong but let user save
                    pass
            elif isinstance(v, dict):
                _item[k] = cast_choices(v, wc)
            elif isinstance(v, list):
                _item[k] = [cast_choices(i, wc) for i in v]

    return _item
