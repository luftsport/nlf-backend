from transitions import Machine

from flask import current_app as app, request
from bson.objectid import ObjectId

from eve.methods.patch import patch_internal

from datetime import datetime, timedelta

from ext.notifications.email import Email  # , Sms
from ext.notifications.notifications import get_recepients, get_recepients_from_roles, get_org_name_text, \
    get_person_name_text

from ext.scf import \
    ACL_SEILFLY_ORS, \
    ACL_SEILFLY_SU, \
    ACL_SEILFLY_CLUB_TEKNISK_LEDER, \
    ACL_SEILFLY_CLUB_OPERATIV_LEDER, \
    ACL_SEILFLY_CLUB_FTL, \
    ACL_SEILFLY_CLUB_SKOLESJEF, \
    ACL_SEILFLY_CLUB_DTO, \
    ACL_SEILFLY_CLUB_FLYTJENESTEN, \
    ACL_CLOSED_ALL_LIST

from ext.app.notifications import ors_workflow
from ext.auth.acl import parse_acl_flat

RESOURCE_COLLECTION = 'seilfly_observations'


def get_wf_init(person_id):
    utc = datetime.utcnow()

    return {'name': 'seilfly_observations_workflow',
            'comment': 'Initialized workflow',
            'state': 'draft',
            'last_transition': utc,
            'expires': utc + timedelta(days=7),
            'settings': {
                'do_not_process_in_club': False,
                'do_not_publish': False
            },
            'audit': [{'a': 'init',
                       'r': 'init',
                       'u': person_id,
                       's': None,
                       'd': 'draft',
                       'v': 1,
                       't': utc,
                       'c': 'Initialized workflow'}]
            }


def get_acl_init(person_id, discipline_id):
    acl = {
        'read': {
            'users': [person_id],
            'roles': [ACL_SEILFLY_ORS]
        },
        'execute': {
            'users': [person_id],
            'roles': []
        },
        'write': {
            'users': [person_id],
            'roles': []
        },
        'delete': {
            'users': [],
            'roles': []
        }
    }
    return acl


WF_SEILFLY_STATES = [
    'draft',
    'pending_review_ors',
    'pending_review_su',
    'pending_review_dto',
    'pending_review_operativ',
    'pending_review_skole',
    'pending_review_teknisk',
    'closed',
    'withdrawn'
]

WF_SEILFLY_STATES_ATTR = {
    'draft': {
        'title': 'Utkast',
        'description': 'Utkast'
    },
    'pending_review_ors': {
        'title': 'Avventer OBSREG',
        'description': 'Avventer OBSREG koordinator'
    },
    'pending_review_su': {
        'title': 'Avventer SU',
        'description': 'Avventer SU'
    },
    'pending_review_dto': {
        'title': 'Avventer DTO',
        'description': 'Avventer DTO ansvarlig i klubb'
    },
    'pending_review_skole': {
        'title': 'Avventer Skolesjef',
        'description': 'Avventer Skolesjef i klubb'
    },
    'pending_review_operativ': {
        'title': 'Avventer Operativ',
        'description': 'Avventer Operativ leder i klubb'
    },
    'pending_review_teknisk': {
        'title': 'Avventer Teknisk',
        'description': 'Avventer Teknisk leder i klubb'
    },
    'withdrawn': {
        'title': 'Trukket',
        'description': 'Observasjonen er trukket'
    },
    'closed': {
        'title': 'Lukket',
        'description': 'Observasjonen er ferdigbehandlet'
    }
}

WF_SEILFLY_TRANSITIONS = [
    # OBSERVATØR
    {'trigger': 'send_to_ors',
     'source': 'draft',
     'dest': 'pending_review_ors',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'withdraw',
     'source': 'draft',
     'dest': 'withdrawn',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'reopen',
     'source': 'withdrawn',
     'dest': 'draft',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    # OBSREGKOOORD
    {'trigger': 'approve_ors',
     'source': 'pending_review_ors',
     'dest': 'closed',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'reopen_ors',
     'source': 'closed',
     'dest': 'pending_review_ors',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'reject_ors',
     'source': 'pending_review_ors',
     'dest': 'draft',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    # SU
    {'trigger': 'send_to_su',
     'source': 'pending_review_ors',
     'dest': 'pending_review_su',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'approve_su',
     'source': 'pending_review_su',
     'dest': 'pending_review_ors',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'reject_su',
     'source': 'pending_review_su',
     'dest': 'pending_review_ors',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    # DTO
    {'trigger': 'send_to_dto',
     'source': 'pending_review_ors',
     'dest': 'pending_review_dto',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'approve_dto',
     'source': 'pending_review_dto',
     'dest': 'pending_review_ors',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'reject_dto',
     'source': 'pending_review_dto',
     'dest': 'pending_review_ors',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },


    # OPERATIVT
    {'trigger': 'send_to_operativ',
     'source': 'pending_review_ors',
     'dest': 'pending_review_operativ',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'approve_operativ',
     'source': 'pending_review_operativ',
     'dest': 'pending_review_ors',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'reject_operativ',
     'source': 'pending_review_operativ',
     'dest': 'pending_review_ors',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    # SKOLE
    {'trigger': 'send_to_skole',
     'source': 'pending_review_operativ',
     'dest': 'pending_review_skole',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'approve_skole',
     'source': 'pending_review_skole',
     'dest': 'pending_review_operativ',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'reject_skole',
     'source': 'pending_review_skole',
     'dest': 'pending_review_operativ',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    # TEKNISK
    {'trigger': 'send_to_teknisk',
     'source': 'pending_review_operativ',
     'dest': 'pending_review_teknisk',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'approve_teknisk',
     'source': 'pending_review_teknisk',
     'dest': 'pending_review_operativ',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },
    {'trigger': 'reject_teknisk',
     'source': 'pending_review_teknisk',
     'dest': 'pending_review_operativ',
     'after': 'save_workflow',
     'conditions': ['has_permission']
     },

]

"""
Resource is bluepring trigger
"""
WF_SEILFLY_TRANSITIONS_ATTR = {
    'send_to_ors': {
        'title': 'Send til Koordinator',
        'action': 'Send til Koordinator',
        'resource': 'approve',
        'comment': True,
        'descr': 'Sendt til ORS Koordinator'
    },
    'withdraw': {
        'title': 'Trekk tilbake observasjon',
        'action': 'Trekk tilbake',
        'resource': 'withdraw',
        'comment': True,
        'descr': 'Trekt tilbake'
    },
    'reopen': {
        'title': 'Gjenåpne observasjon',
        'action': 'Gjenåpne',
        'resource': 'reopen',
        'comment': True,
        'descr': 'Gjenåpnet'
    },
    'reopen_ors': {
        'title': 'Gjenåpne observasjon',
        'action': 'Gjenåpne',
        'resource': 'reopen',
        'comment': True,
        'descr': 'Gjenåpnet'
    },
    'approve_ors': {
        'title': 'Godkjenn observasjon',
        'action': 'Lukk',
        'resource': 'approve',
        'comment': True,
        'descr': 'Godkjent av ORS Koordinator'
    },
    'reject_ors': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt tilbake av ORS koord'
    },
    'send_to_su': {
        'title': 'Send til SU',
        'action': 'Send til SU',
        'resource': 'su',
        'comment': True,
        'descr': 'Sendt til SU'
    },
    'approve_su': {
        'title': 'Godkjent SU',
        'action': 'Send til Koordinator',
        'resource': 'approve',
        'comment': True,
        'descr': 'Sendt til ORS Koordinator'
    },
    'reject_su': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt til ORS Koordinator'
    },
    'send_to_dto': {
        'title': 'Send til DTO',
        'action': 'Send til DTO',
        'resource': 'dto',
        'comment': True,
        'descr': 'Sendt til DTO ansvarlig'
    },
    'approve_dto': {
        'title': 'Godkjent DTO',
        'action': 'Godkjenn',
        'resource': 'approve',
        'comment': True,
        'descr': 'Godkjent'
    },
    'reject_dto': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt til OBSREG Koordinator'
    },
    'send_to_operativ': {
        'title': 'Send til Operativ Leder',
        'action': 'Send til Operativ Leder',
        'resource': 'operativ',
        'comment': True,
        'descr': 'Sendt til Operativ Leder'
    },
    'approve_operativ': {
        'title': 'Godkjent Operativ',
        'action': 'Godkjenn',
        'resource': 'approve',
        'comment': True,
        'descr': 'Sendt til OBSREG Koordinator'
    },
    'reject_operativ': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt til OBSREG Koordinator'
    },
    'send_to_skole': {
        'title': 'Send til Skolesjef',
        'action': 'Send til Skolesjef',
        'resource': 'skole',
        'comment': True,
        'descr': 'Sendt til Skolesjef'
    },
    'approve_skole': {
        'title': 'Godkjent Skolesjef',
        'action': 'Godkjenn',
        'resource': 'approve',
        'comment': True,
        'descr': 'Sendt til Operativ Leder',
    },
    'reject_skole': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt til DTO'
    },
    'send_to_teknisk': {
        'title': 'Send til Teknisk Leder',
        'action': 'Send til Teknisk Leder',
        'resource': 'teknisk',
        'comment': True,
        'descr': 'Sendt til Teknisk Leder'
    },
    'approve_teknisk': {
        'title': 'Godkjent Teknisk',
        'action': 'Godkjenn',
        'resource': 'approve',
        'comment': True,
        'descr': 'Sendt til Operativ Leder'
    },
    'reject_teknisk': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt til Operativ Leder'
    }


}


class ObservationWorkflow(Machine):
    """ For further work, should use https://github.com/einarhuseby/transitions instead of https://github.com/tyarkoni/transitions
    This fork will support the requirements in this project and also keep track of origin
    @todo: add https://github.com/einarhuseby/transitions to site-packages
    @todo: pip install git+https://github.com/einarhuseby/transitions
    """

    def __init__(self, object_id=None, initial_state=None, user_id=None, comment=None):

        self.user_id = user_id
        # The states
        # states 'name', 'on_enter', 'on_exit'
        self._states = WF_SEILFLY_STATES

        self._state_attrs = WF_SEILFLY_STATES_ATTR

        """ The transition definition
        """
        self._transitions = WF_SEILFLY_TRANSITIONS

        self.action = None
        """ Extra attributes needed for sensible feedback from API to client
        """
        self._trigger_attrs = WF_SEILFLY_TRANSITIONS_ATTR

        """ Make sure to start with a defined state!
        """
        col = app.data.driver.db[RESOURCE_COLLECTION]

        self.db_wf = col.find_one({'_id': ObjectId(object_id)},
                                  {'id': 1,
                                   'workflow': 1,
                                   'acl': 1,
                                   'club': 1,
                                   'discipline': 1,
                                   '_etag': 1,
                                   '_version': 1,
                                   '_model': 1,
                                   'owner': 1,
                                   'reporter': 1,
                                   'organization': 1,
                                   'tags': 1,
                                   'acl': 1}
                                  )

        initial_state = self.db_wf.get('workflow', {}).get('state', None)

        if initial_state == None or initial_state not in self._states:
            self.initial_state = 'draft'
        else:
            self.initial_state = initial_state

        # Set defaults from
        self.ors = self.db_wf.get('organization', {}).get('ors', None)
        self.reporter = self.db_wf.get('reporter', None)
        self.owner = self.db_wf.get('owner', None)
        self.club = self.db_wf.get('club', None)
        self.discipline = self.db_wf.get('discipline', None)

        # Backporting
        self.wf_settings = self.db_wf.get('workflow', {}).get('settings', {
            'do_not_process_in_club': False,
            'do_not_publish': False
        })

        self.acl_ORS = ACL_SEILFLY_ORS.copy()
        # self.acl_ORS['org'] = self.discipline

        self.acl_SKOLE = ACL_SEILFLY_CLUB_SKOLESJEF.copy()
        self.acl_SKOLE['org'] = self.discipline

        self.acl_DTO = ACL_SEILFLY_CLUB_DTO.copy()
        self.acl_DTO['org'] = self.discipline

        self.acl_TEKNISK = ACL_SEILFLY_CLUB_TEKNISK_LEDER.copy()
        self.acl_TEKNISK['org'] = self.discipline

        self.acl_OPERATIV = ACL_SEILFLY_CLUB_OPERATIV_LEDER.copy()
        self.acl_OPERATIV['org'] = self.discipline

        self.acl_SU = ACL_SEILFLY_SU.copy()
        self.acl_SU['org'] = self.discipline

        self.initial_acl = self.db_wf.get('acl', {}).copy()

        self.comment = '' if comment is None else '{}'.format(comment).strip()

        Machine.__init__(self,
                         states=self._states,
                         send_event=True,
                         transitions=self._transitions,
                         initial=self.initial_state)

    def get_actions(self):

        events = []
        for transition in self._transitions:
            if self.state in transition['source']:
                events.append(transition['trigger'])

        return events

    def get_resource_mapping(self):
        """ This will return a dict containing a mapping of resource => trigger
        Example: {'approve': 'approval_from_someone'}
        resource should be utilised in the endpoint/resource and trigger is the callee trigger method in the workflow
        """
        events = {}
        for transition in self._transitions:
            if self.state in transition.get('source', None):
                events.update({self._trigger_attrs.get(transition['trigger']).get('resource'): transition['trigger']})

        return events

    def get_resources(self):

        resources = []

        for event in self.get_actions():
            tmp = self._trigger_attrs.get(event)
            if self.initial_state=='pending_review_ors' and event=='send_to_ftl':
                tmp['permission'] = self.has_permission(None) and self.can_process_in_club(None)
            else:
                tmp['permission'] = self.has_permission(None)

            resources.append(tmp)

        return resources

    def get_current_state(self):

        d = {'state': self.state}
        d.update(self._state_attrs[self.state])
        d.update({'actions': self.get_resources()})

        return d

    def get_allowed_users_for_transitions(self):

        # Should return users allowed for this transition!
        return NotImplemented

    def has_permission(self, event):
        """ No events sendt by conditions...
        if event.kwargs.get('user_id', 0) in self.trigger_permissions:
            return True
        return False
        check if in execute!
        """
        try:
            if len([i for i in app.globals['acl'].get('roles', []) if i in self.initial_acl['execute']['roles']]) > 0 \
                    or app.globals['user_id'] in self.initial_acl['execute']['users']:
                return True
        except Exception as e:
            # print('ERRRRR', e)
            pass

        return False

        # return acl_has_permission(self.db_wf['_id'], 'execute', 'observations')

    def can_process_in_club(self, event):
        return not self.wf_settings.get('do_not_process_in_club', False)

    def condition_completed_tasks(self):

        # Check if has completed all tasks,
        # Have "current tasks" and then

        raise NotImplementedError

        return self.db_wf['workflow']['audit']

    def get_audit(self):

        # Get which trigger where done, and by who?
        # This is called before the save_state

        trail = {'audit': self.db_wf['workflow']['audit']}

        return trail

    def save_state(self):

        # app.data... update OR patch_internal
        # Save *.workflow dictionary

        raise NotImplemented

    def set_acl(self):

        """Use self.initial_state as from state!"""

        acl = self.db_wf.get('acl', {})
        reporter = self.db_wf.get('reporter')

        if self.state == 'draft':
            """Only owner can do stuff?"""

            acl['read']['users'] += [reporter]
            acl['write']['users'] = [reporter]
            acl['execute']['users'] = [reporter]

            acl['read']['roles'] += [self.acl_ORS]
            acl['write']['roles'] = []
            acl['execute']['roles'] = []


        elif self.state == 'withdrawn':
            """ Only owner! """
            acl['write']['users'] = []
            acl['read']['users'] = [reporter]
            acl['execute']['users'] = [reporter]

            acl['write']['roles'] = []
            acl['read']['roles'] = []
            acl['execute']['roles'] = []


        # Only set fixed
        elif self.state == 'pending_review_ors':
            """ Owner, reporter read, fsj read, hi read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []

            # Only reporter can make
            if self.wf_settings.get('do_not_process_in_club', False) is False:
                if self.initial_state == 'closed':
                    acl['read']['roles'] = [self.acl_ORS, self.acl_OPERATIV]
                else:
                    acl['read']['roles'] += [self.acl_ORS, self.acl_OPERATIV]
            else:
                if self.initial_state == 'closed':
                    acl['read']['roles'] = [self.acl_ORS]
                else:
                    acl['read']['roles'] += [self.acl_ORS]
                    acl['read']['roles'] += [self.acl_ORS]

            acl['write']['roles'] = [self.acl_ORS]
            acl['execute']['roles'] = [self.acl_ORS]

        elif self.state == 'pending_review_su':

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['write']['roles'] = [self.acl_SU]
            acl['read']['roles'] += [self.acl_ORS, self.acl_SU]
            acl['execute']['roles'] = [self.acl_SU]

        elif self.state == 'pending_review_dto':

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['write']['roles'] = [self.acl_DTO]
            acl['read']['roles'] += [self.acl_ORS, self.acl_DTO]
            acl['execute']['roles'] = [self.acl_DTO]

        elif self.state == 'pending_review_operativ':

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['write']['roles'] = [self.acl_OPERATIV]
            acl['read']['roles'] += [self.acl_ORS, self.acl_OPERATIV]
            acl['execute']['roles'] = [self.acl_OPERATIV]

        elif self.state == 'pending_review_skole':

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['write']['roles'] = [self.acl_SKOLE]
            acl['read']['roles'] += [self.acl_ORS, self.acl_OPERATIV, self.acl_SKOLE]
            acl['execute']['roles'] = [self.acl_SKOLE]

        elif self.state == 'pending_review_teknisk':

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['write']['roles'] = [self.acl_TEKNISK]
            acl['read']['roles'] += [self.acl_ORS, self.acl_OPERATIV, self.acl_TEKNISK]
            acl['execute']['roles'] = [self.acl_TEKNISK]


        elif self.state == 'closed':

            # acl['read']['users'] = [] #Should let users still see??
            acl['write']['users'] = []
            acl['execute']['users'] = []

            # Only if we can make it public
            if self.wf_settings.get('do_not_publish', False) is False:
                acl['read']['roles'] += ACL_CLOSED_ALL_LIST

            acl['write']['roles'] = []
            acl['execute']['roles'] = [self.acl_ORS]

        # Sanity - should really do list comprehension...
        acl['read']['users'] = list(set(acl['read']['users']))
        acl['write']['users'] = list(set(acl['write']['users']))
        acl['execute']['users'] = list(set(acl['execute']['users']))

        acl['read']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['read']['roles'])]
        acl['write']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['write']['roles'])]
        acl['execute']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['execute']['roles'])]

        return acl

    def save_workflow(self, event):
        """ Will only trigger when it actually IS changed, so save every time this is called!
        patch_internal(self.known_resource, data, concurrency_check=False,**{'_id': self.item_id})
        patch_internal(resource, payload=None, concurrency_check=False,skip_validation=False, **lookup):

        Hmmm, need audit trail since version control will not cut this. Workflow should also increase the version number
        """
        _id = self.db_wf.get('_id')
        _etag = self.db_wf.get('_etag')
        _version = self.db_wf.get('_version')
        self.action = event.event.name

        self.db_wf.get('workflow').update({'state': self.state})

        # Make a new without _id etc
        new = {'workflow': self.db_wf.get('workflow')}

        audit = {'a': event.event.name,
                 'r': self._trigger_attrs.get(event.event.name).get('resource'),
                 'u': self.user_id,
                 's': self.initial_state,
                 'd': self.state,
                 'v': _version + 1,
                 't': datetime.utcnow(),
                 'c': self.comment}

        new['workflow']['audit'].insert(0, audit)

        new['workflow']['last_transition'] = datetime.utcnow()

        # New owner it is!
        new['owner'] = app.globals['user_id']

        if self._trigger_attrs.get(event.event.name).get('comment', False):
            new.get('workflow').update({'comment': self.comment})

        # Always add
        new['workflow']['settings'] = self.wf_settings

        new['acl'] = self.set_acl()

        # Should really supply the e-tag here, will work! , '_etag': _etag
        # Can also use test_client to do this but it's rubbish or?
        # This will ignore the readonly field skip_validation AND you do not need another domain file for it!!
        response, last_modified, etag, status = patch_internal(RESOURCE_COLLECTION,
                                                               payload=new,
                                                               concurrency_check=False,
                                                               skip_validation=True,
                                                               **{'_id': "%s" % _id, '_etag': "%s" % _etag})
        # test_client().post('/add', data = {'input1': 'a'}}
        # app.test_client().patch('/observations/%s' % _id, data=new, headers=[('If-Match', _etag)])

        # if self.state != self.initial_state:

        if status in [200, 201]:
            self.notification()
            return True

        return False

    def notify_created(self):
        self.notification(action='init',
                          context='created')

    def notification(self, action=None, context='transition'):

        # get users from roles
        # ors_workflow(recepients, activity, _id, action, source, destination, comment, context='transition')

        if action is None:
            action = WF_SEILFLY_TRANSITIONS_ATTR[self.action]['resource']

        # Not to self!
        # If closed - notify ONLY existing acl's

        if self.state == 'closed':
            tmp = self.db_wf.get('acl', {})
            tmp['read']['roles'] = [x for x in tmp['read']['roles'] if x not in ACL_CLOSED_ALL_LIST]
            acl = parse_acl_flat(tmp)
        else:
            acl = parse_acl_flat(self.db_wf.get('acl', {}))

        ors_workflow(
            recepients=acl,  # notify self too!
            event_from=RESOURCE_COLLECTION,
            event_from_id=self.db_wf['_id'],
            ors_id=self.db_wf['id'],
            org_id=self.db_wf.get('discipline'),
            ors_tags=self.db_wf.get('tags', []),
            action=action,
            source=self.initial_state,  # self._state_attrs[self.initial_state]['description'],
            destination=self.state,  # self._state_attrs[self.state]['description'],
            comment=self.comment,
            context=context
        )
