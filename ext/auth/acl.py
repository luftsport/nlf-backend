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

def get_acl(collection, _id):
    col = app.data.driver.db[collection]
    # db.companies.find().skip(NUMBER_OF_ITEMS * (PAGE_NUMBER - 1)).limit(NUMBER_OF_ITEMS )

    oid = ObjectId(_id)
    if oid == ObjectId(str(oid)):
        match = {'_id': oid}
    else:
        match = {'id': _id}

    print(match)
    res = col.find_one({'$and': [match,
                                 {'$or':
                                     [
                                         {'acl.read.users': {'$in': [app.globals['user_id']]}},
                                         {'acl.read.roles': {'$in': app.globals['acl']['roles']}}
                                     ]
                                 }
                                 ]
                        },
                       {'acl': 1}
                       )

    try:
        return True, res['acl']
    except Exception as e:
        return False, None



def parse_acl(acl):
    users = {
        'read': acl.get('read', {}).get('users', []),
        'write': acl.get('write', {}).get('users', []),
        'execute': acl.get('execute', {}).get('users', []),
        'delete': acl.get('delete', {}).get('users', []),
    }

    for right in acl.keys():
        print('RIGHT', right)
        for role in acl.get(right, {}).get('roles', []):
            print('ROLE', role)

            if role.get('org', 0) > 0:
                _orgs = [role.get('org')]
            elif role.get('club', 0) > 0:
                _orgs = [role.get('club')]
            else:
                _orgs = get_orgs_in_activivity(role.get('activity'))

            users[right] += get_users_from_role(role.get('role'), _orgs)

        acl[right] = list(set(acl[right]))

    return users

def has_permission(id, type, collection):
    """ Checks if current user has type (execute, read, write) permissions on an collection or not
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
        if len([i for i in app.globals['acl']['roles'] if i in acl['acl'][type]['roles']]) > 0 \
                or app.globals['user_id'] in acl['acl'][type]['users']:
            return True
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
        if collection not in ['observations', 'users']:
            collection = 'observations'

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
