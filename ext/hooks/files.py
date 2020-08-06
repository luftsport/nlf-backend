from ext.auth.acl import has_permission
from ext.app.eve_helper import eve_abort


def after_fetched_item(response):
    try:

        response = _anon(response)

    except Exception as e:
        print('Error', e)
        return eve_abort(500, 'Anon file aborted')


def after_fetched_list(response):
    try:
        for key, item in enumerate(response.get('_items', [])):
            response['_items'][key] = _anon(item)
    except Exception as e:
        print('Error', e)
        return eve_abort(500, 'Anon file aborted')


def _anon(file_dict):
    if has_permission(file_dict['ref_id'], 'write', file_dict['ref']) is False:
        file_dict.pop('owner', None)

    return file_dict
