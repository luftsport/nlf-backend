"""

    ACL functions
    =============
    
    @see: blueprints/acl.py for use
    
    @todo: Make this more solid!
    @todo: Handle id and _id gracefully
"""

from flask import current_app as app
from bson.objectid import ObjectId
from ext.app.lungo import get_users_from_role, get_orgs_in_activivity
from ext.scf import ACL_NANON_ROLES

def get_acl(collection, _id, projection={'acl': 1}, right='read'):
    acl = {}
    res = {}
    col = app.data.driver.db[collection]
    # db.companies.find().skip(NUMBER_OF_ITEMS * (PAGE_NUMBER - 1)).limit(NUMBER_OF_ITEMS )

    oid = ObjectId(_id)
    if oid == ObjectId(str(oid)):
        match = {'_id': oid}
    else:
        match = {'id': _id}

    # print('MATCH', match)
    res = col.find_one({'$and': [match,
                                 {'$or':
                                     [
                                         {'acl.{}.users'.format(right): {'$in': [app.globals['user_id']]}},
                                         {'acl.{}.roles'.format(right): {'$in': app.globals['acl']['roles']}}
                                     ]
                                 }
                                 ]
                        },
                       projection
                       )

    try:
        acl = res.pop('acl', None)
        return True, acl, res
    except Exception as e:
        return False, None, None


def modify_user_acl(collection, _id, person_id, right, operation):
    if right not in ['read', 'write'] or int(person_id) != person_id or operation not in ['add', 'delete', 'remove']:
        return False

    col = app.data.driver.db[collection]

    try:
        oid = ObjectId(_id)
        if oid == ObjectId(str(oid)):
            match = {'_id': oid}
        else:
            match = {'id': _id}

        if operation == 'add':
            res = col.update(match, {'$addToSet': {'acl.{}.users'.format(right): int(person_id)}})
        elif operation in ['delete', 'remove']:
            res = col.update(match, {'$pull': {'acl.{}.users'.format(right): {'$in': [person_id]}}})

        return True
    except Exception as e:
        # print('ERRR', e)
        pass
    return False


def parse_acl(acl):

    users = {
        'read': acl.get('read', {}).get('users', []),
        'write': acl.get('write', {}).get('users', []),
        'execute': acl.get('execute', {}).get('users', []),
        'delete': acl.get('delete', {}).get('users', []),
    }

    for right in acl.keys():
        # print('RIGHT', right)
        for role in acl.get(right, {}).get('roles', []):
            # print('ROLE', role)

            if role.get('org', None) is not None and role.get('org', 0) > 0:
                _orgs = [role.get('org')]
            elif role.get('club', None) is not None and role.get('club', 0) > 0:
                _orgs = [role.get('club')]
            else:
                _orgs = get_orgs_in_activivity(role.get('activity', 0))

            users[right] += get_users_from_role(role.get('role'), _orgs)

        acl[right] = list(set(acl[right]))


    return users


def parse_acl_flat(acl, exclude_current_user=False):
    """Parses acl then flattens to list of users"""
    res = parse_acl(acl)

    if exclude_current_user is True:
        return [p for p in list(set(res['read'] + res['write'] + res['execute'] + res['delete'])) if p != app.globals.get('user_id', 0)]

    return [p for p in list(set(res['read'] + res['write'] + res['execute'] + res['delete']))]

def _has_permission(resource_acl, perm):
    """@TODO Global"""
    if (
            any(pid for pid in app.globals['acl']['roles'] if pid in resource_acl[perm]['roles']) is True
            or (app.globals['user_id'] in resource_acl[perm]['users']) is True
    ):
        return True
    return False


def has_nanon_permission(resource_acl, perm, state, model, org=0):
    """Closed who should be able to see non-anon?
    org=0 will make roles for all org True"""

    try:
        roles = []
        for role in ACL_NANON_ROLES.get(model, []):
            if role['org'] == 0:
                role['org'] = org
            roles.append(role)

        if state == 'closed' and perm == 'execute':
            # print('NANON', [pid for pid in app.globals['acl']['roles'] if pid in roles])
            # print(app.globals['user_id'] in resource_acl[perm]['roles'])
            if (
                    any(pid for pid in app.globals['acl']['roles'] if pid in roles) is True
                    or app.globals['user_id'] in resource_acl[perm]['roles'] is True
            ):
                return True

        return _has_permission(resource_acl, perm)
    except:
        pass

    return False

def has_permission(id, permission_type, collection):
    """ Checks if current user has type (execute, read, write, delete) permissions on an collection or not
    @note: checks on list comprehension and returns number of intersects in list => len(list) > 0 == True
    @bug: Possible bug if user comparison is int vs float!
    """

    col = app.data.driver.db[collection]

    # We can find by id and _id
    try:
        o = ObjectId(id)
        if o == ObjectId(str(o)):
            acl = col.find_one({'_id': ObjectId(id)}, {'acl': 1})
        else:
            acl = col.find_one({'id': id}, {'acl': 1})

    except:
        acl = col.find_one({'id': id}, {'acl': 1})
        pass

    acl = col.find_one({'_id': ObjectId(id)}, {'acl': 1})
    try:
        # if len([i for i in app.globals['acl']['roles'] if i in acl['acl'][type]['roles']]) > 0 \
        #        or app.globals['user_id'] in acl['acl'][type]['users']:
        #    return True
        return _has_permission(acl['acl'], permission_type)
    except:
        return False

    return False


def get_user_acl_mapping(acl) -> dict:
    """Input acl object"""

    x = False
    w = False
    r = False
    d = False

    try:
        if len([i for i in app.globals['acl']['roles'] if i in acl['execute']['roles']]) > 0 \
                or app.globals['user_id'] in acl['execute']['users']:
            x = True
    except:
        pass

    try:
        if len([i for i in app.globals['acl']['roles'] if i in acl['read']['roles']]) > 0 \
                or app.globals['user_id'] in acl['read']['users']:
            r = True
    except:
        pass

    try:
        if len([i for i in app.globals['acl']['roles'] if i in acl['write']['roles']]) > 0 \
                or app.globals['user_id'] in acl['write']['users']:
            w = True
    except:
        pass

    try:
        if len([i for i in app.globals['acl']['roles'] if i in acl['delete']['roles']]) > 0 \
                or app.globals['user_id'] in acl['delete']['users']:
            d = True
    except:
        pass

    return {'r': r, 'w': w, 'x': x, 'd': d}


def get_user_permissions(_id, collection):
    """
    len([pid for pid in app.globals[all_person_ids] if pid in ])
    eller
    any(pid for pid in dict1 if pid in dict2)
    :param id:
    :param collection:
    :return:
    """
    try:
        if collection not in ['fallskjerm_observations', 'motorfly_observations' 'users']:
            collection = 'fallskjerm_observations'

        col = app.data.driver.db[collection]

        try:
            o = ObjectId(_id)
            if o == ObjectId(str(o)):
                acl = col.find_one({'_id': ObjectId(_id)}, {'acl': 1, 'id': 1, '_id': 1})
            else:
                acl = col.find_one({'id': _id}, {'acl': 1, 'id': 1, '_id': 1})

        except:
            acl = col.find_one({'id': _id}, {'acl': 1, 'id': 1, '_id': 1})
            pass

        try:
            mapping = get_user_acl_mapping(acl['acl'])
        except:
            mapping = {'r': False, 'w': False, 'x': False, 'd': False}

        return {'id': acl['id'], '_id': acl['_id'], 'resource': collection, 'u': app.globals['user_id'],
                'r': mapping['r'], 'w': mapping['w'], 'x': mapping['x'], 'd': mapping['d']}


    except:
        return {'_error': {'code': 404,
                           'message': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'}, \
                '_status': 'ERR'}

    return result


def user_persmissions(resource_acl, state):
    permissions = {
        'read': False,
        'write': False,
        'delete': False,
        'execute': False,
    }

    for perm in permissions.keys():
        permissions[perm] = has_nanon_permission(resource_acl, perm, state)

    return permissions



