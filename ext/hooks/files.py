from ext.auth.acl import has_permission, has_obsreg_file_permission
from ext.app.eve_helper import eve_abort
from flask import abort


def before_insert_item(item):
    item['owner'] = g.id


def after_fetched_item(response):
    try:

        response = _anon(response)
        if 'observations' in response.get('ref', ''):
            if has_obsreg_file_permission(response.get('_id', None), response.get('ref_id', None), response.get('activity', None), 'read') is False:
                abort(403, 'You do not have permission to access this file')


    except Exception as e:
        abort(403, 'You do not have permission to access this file')


def after_fetched_list(response):
    try:
        for key, item in enumerate(response.get('_items', [])):
            response['_items'][key] = _anon(item)
            if 'observations' in item.get('ref', ''):
                if has_obsreg_file_permission(item.get('_id', None), item.get('ref_id', None), item.get('activity', None), 'read') is False:
                    print('Removing file from list due to permission: %s' % item.get('_id', None))
                    response['_items'] = [x for x in response['_items'] if x.get('_id', None) != item.get('_id', None)]

    except Exception as e:
        eve_abort(500, 'Server error, file retrival aborted')


def _anon(file_dict):
    if has_permission(file_dict['ref_id'], 'write', file_dict['ref']) is False:
        file_dict.pop('owner', None)

    return file_dict
