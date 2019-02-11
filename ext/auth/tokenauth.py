"""
    Token based Auth
    ================
    
    Also ACL added!!
    
    @attention: Needs tokenmaster to issue tokens
"""

# Atuhentication
from eve.auth import TokenAuth
from flask import current_app as app, request, Response, abort
# from eve.methods.get import getitem as get_internal
# from bson.objectid import ObjectId
from ext.auth.helpers import Helpers
# TIME & DATE - better with arrow only?

import arrow


class TokenAuth(TokenAuth):
    is_auth = False
    person_id = None

    def check_auth(self, token, allowed_roles, resource, method):
        """Simple token check. Tokens comes in the form of request.authorization['username']
        Token is decoded request.authorization['username']
        """
        # Needs to check token exists and equals request AND valid is in the future!
        # Token expired error
        # Token error
        # Set acl to the global XXX for use in all pre_ db lookup queries!
        # Can also get the database lookup for the resource and check that here!!
        # Can also issue a new token here, and that needs to be returned by injecting to pre dispatch
        # use the abort/eve_error_msg to issue errors!

        accounts = app.data.driver.db[app.globals['auth']['auth_collection']]

        u = accounts.find_one({'auth.token': token})

        if u:

            self.person_id = u['id']

            utc = arrow.utcnow()
            if utc.timestamp < arrow.get(u['auth']['valid']).timestamp:

                valid = utc.replace(seconds=+app.config['AUTH_SESSION_LENGHT'])

                # If it fails, then token is not renewed
                accounts.update_one({'_id': u['_id']}, {"$set": {"auth.valid": valid.datetime}})

                # For use in pre_insert/update - handled in set_acl
                # app.globals.update({'id': u['id']})
                # app.globals.update({'_id':  u['_id']})

                # Set acl
                app.globals.update({'user_id': u['id']})
                # self.set_acl(u['acl'], u['_id'], u['id'])
                self._set_globals(u['id'], u['user'])

                # Set acl - use id to make sure
                self.set_acl(u)

                # See if needed for the resource
                # Contains per method (ie read or write or all verbs)
                """
                if allowed_roles:

                    helper = Helpers()
                    local_roles = []
                    for role in allowed_roles:
                        local_roles.extend(helper.get_all_users_in_role_by_ref(ref=role))

                    if len(local_roles) == 0 or u['id'] not in local_roles:
                        self.is_auth = False
                        return False
                """
                self.is_auth = True

                # Set request auth value IF on users resource
                # This effectively limits all operations except GET
                # hence only the authenticated user can change the corresponding users item (by id)
                # @note: This corresponds to domain definition 'auth_field': 'id'
                if method != 'GET' and resource == 'users':
                    self.set_request_auth_value(u['id'])

                # This allows oplog to push u = id (membership #)
                self.set_user_or_token(u['id'])

                return True  # Token exists and is valid, renewed for another hour

            else:  # Expired validity
                return False

        return False

    def get_user_id(self):
        return self.person_id

    def _set_globals(self, id, _id):
        app.globals.update({'id': id})
        app.globals.update({'_id': "%s" % _id})

    def authenticate(self):
        """ Overridden by NOT returning a WWW-Authenticate header
        This makes the browser NOT fire up the basic auth
        """
        resp = Response(None, 401)
        abort(401, description='Please provide proper credentials', response=resp)

    def set_acl(self, u):
        """ Sets the acl dict on the current authenticated user
        Needs to get clubs from melwin in order to sport the acl_groups.ref link
        """
        # Get users acl
        # col = app.data.driver.db[app.globals['auth']['users_collection']]
        # user = col.find_one({'id': u['id']}, {'acl': 1})
        # app.globals['acl'] = {'roles': user.get('acl', [])}

        if u['id'] == 301041:
            # app.globals['acl']['roles'] = ['5857158426867a5adfc40550']
            # SU

            u['acl'].append({"activity": 109,
                             "club": 0,
                             "role": 999})
            u['acl'].append({"activity": 0,
                             "club": 0,
                             "role": 999})

            # HI
            """
            u['acl'].append({"activity": 109,
                             "club": 24779,
                             "role": 201120})
            u['acl'].append({"activity": 109,
                             "club": 0,
                             "role": 201120})
            u['acl'].append({"activity": 0,
                             "club": 0,
                             "role": 201120})
            """
        app.globals['acl'] = {'roles': u['acl']}
        return

        # Aarg need to remove name and func!!!
        acl_ = user.get('acl_roles', [])
        acl = []
        for role in acl_:
            # Seksjon og klubb
            acl.append({"activity": role['activity'],
                        "club": role['club'],
                        "role": role['role']})
            # Seksjon
            acl.append({"activity": role['activity'],
                        "club": 0,
                        "role": role['role']})
            # Kun rolle
            acl.append({"activity": 0,
                        "club": 0,
                        "role": role['role']})

        # TO BE REMOVED
        if person_id == 301041:
            # app.globals['acl']['roles'] = ['5857158426867a5adfc40550']
            # SU
            acl.append({"activity": 109,
                        "club": 0,
                        "role": 999})
            acl.append({"activity": 0,
                        "club": 0,
                        "role": 999})
            # HI
            """
            acl.append({"activity": 109,
                        "club": 24779,
                        "role": 201120})
            acl.append({"activity": 109,
                        "club": 0,
                        "role": 201120})
            acl.append({"activity": 0,
                        "club": 0,
                        "role": 201120})
            """

        # print(acl)

        app.globals['acl'] = {'roles': acl}

        # LEGACY below, needed for fallskjerm
        # return

        # Get users acl
        # col = app.data.driver.db[app.globals['auth']['users_collection']]
        # user = col.find_one({'melwin_id': user.get('melwin_id', 0)}, {'acl': 1})
        # acl = user['acl']

        # Now get from all clubs!
        # melwin = app.data.driver.db['legacy_melwin_users']
        # melwin_user = melwin.find_one({'id': user.get('melwin_id', 0)}, {'membership': 1})
        # print('Melwin Id', user.get('melwin_id', 0))

        # acl['roles'] = list(set(acl['roles']))

        # app.globals.update({'acl': acl})

    def _set_acl(self, acl, _person_id, person_id):

        if acl:
            app.globals.update({'acl': acl})

        raise NotImplemented
