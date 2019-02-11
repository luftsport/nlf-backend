from eve.methods.post import post_internal
from ext.app.eve_helper import eve_abort, is_mongo_alive
import ext.app.lungo as lungo

USER_COLLECTION = 'users'


class User:
    user = None
    person_id = None
    acl = []
    merged_from = []

    def __init__(self, person_id, app):

        self.app = app
        self.client = app.data.driver.db
        self.col = self.client[app.globals['auth']['users_collection']]

        try:
            # user, last_modified, etag, status = getitem_internal(resource='users', **{'id': person_id})
            user_ = list(self.col.find({'id': person_id}))
            if len(user_) == 1:
                self.user = user_[0]
            elif user_ is None or len(user_) == 0:
                status, merged_from = lungo.get_person_merged_from(person_id)
                if status is True and len(merged_from) > 0:
                    status, person_from_merged = self.get_merged_user(merged_from)
                    if status is True and len(person_from_merged) > 0:
                        self.user = person_from_merged
                    else:
                        self.user = self._create_user(person_id)
                else:
                    self.user = self._create_user(person_id)

            else:
                eve_abort(500, 'Error getting the user')
            self.person_id = person_id
        except Exception as e:
            if not is_mongo_alive():
                eve_abort(502, 'Network problems')

    def _create_user(self, person_id):
        # melwin_user, _, _, status = getitem_internal(resource='legacy_melwin_users', **{'id': person_id})

        status, resp = lungo.get_person(person_id)

        if status is True:
            try:

                _, self.acl = lungo.get_person_acl(person_id)
                _, self.merged_from = lungo.get_person_merged_from(person_id)

                # Insert new person
                user_response, _, _, user_code, _ = post_internal(resource=self.app.globals['auth']['users_collection'],
                                                                  payl={'id': person_id,
                                                                        'acl': self.acl,
                                                                        'settings': {},
                                                                        'merged_from': self.merged_from,
                                                                        'last_person_id': person_id},
                                                                  skip_validation=True)
                if user_code == 201:
                    # Create auth record for user
                    auth_response, _, _, auth_code, _ = post_internal(resource='users_auth',
                                                                      payl={'id': person_id,
                                                                            'user': user_response['_id'],
                                                                            'acl': self.acl,
                                                                            'auth': {"token": "",
                                                                                     "valid": ""}},
                                                                      skip_validation=True)

                    if auth_code == 201:
                        # All good!!
                        return self.col.find_one({'id': person_id})

            except Exception as e:
                self.app.logger.exception("503 Could not create (POST) new user %i" % person_id)

        return None

    def _delete_user(self, person_id):
        pass

    def get_merged_user(self, merged_persons):

        try:
            users = list(self.col.find({'id': {'$in': merged_persons}}))

            if users and len(users) == 1:
                return True, users[0]  # ['id']
            elif users and len(users) > 1:
                self.app.logger.error('Too many users found')
        except:
            pass

        return False, None
