from transitions import Machine

from flask import current_app as app, request
from bson.objectid import ObjectId

from eve.methods.patch import patch_internal

from datetime import datetime

import re

from ext.auth.helpers import Helpers
from ext.auth.acl import has_permission as acl_has_permission
from ext.notifications.email import Email  # , Sms
from ext.scf import ACL_CLOSED_ALL, ACL_FALLSKJERM_FSJ, ACL_FALLSKJERM_HI, ACL_FALLSKJERM_SU
import arrow

RESOURCE_COLLECTION = 'fallskjerm_observations'


def get_wf_init(person_id):
    utc = arrow.utcnow()

    return {'name': 'ObservationWorkflow',
            'comment': 'Initialized workflow',
            'state': 'draft',
            'last_transition': utc.datetime,
            'expires': utc.replace(days=+7).datetime,
            'audit': [{'a': 'init',
                       'r': 'init',
                       'u': person_id,
                       's': None,
                       'd': 'draft',
                       'v': 1,
                       't': utc.datetime,
                       'c': 'Initialized workflow'}]
            }


def get_acl_init(person_id, club_id):
    hi_role = ACL_FALLSKJERM_HI.copy()
    hi_role['club'] = club_id
    acl = {
        'read': {
            'users': [person_id],
            'roles': [hi_role]
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


WF_FALLSKJERM_STATES = ['draft', 'pending_review_hi', 'pending_review_fs', 'pending_review_su', 'closed', 'withdrawn']

WF_FALLSKJERM_ATTR = {'draft': {'title': 'Utkast', 'description': 'Utkast'},
                      'pending_review_hi': {'title': 'Avventer HI', 'description': 'Avventer vurdering HI'},
                      'pending_review_fs': {'title': 'Avventer Fagsjef',
                                            'description': 'Avventer vurdering Fagsjef'},
                      'pending_review_su': {'title': 'Avventer SU', 'description': 'Avventer vurdering SU'},
                      'closed': {'title': 'Lukket', 'description': 'Observasjonen er lukket'},
                      'withdrawn': {'title': 'Trukket', 'description': 'Observasjonen er trekt tilbake'},
                      }
WF_FALLSKJERM_TRANSITIONS = [
    # { 'trigger': 'set_ready', 'source': 'draft', 'dest': 'ready', 'after': 'save_workflow', 'conditions':['has_permission']},
    {'trigger': 'send_to_hi', 'source': 'draft', 'dest': 'pending_review_hi', 'after': 'save_workflow',
     'conditions': ['has_permission']},
    {'trigger': 'withdraw', 'source': ['draft'], 'dest': 'withdrawn', 'after': 'save_workflow',
     'conditions': ['has_permission']},
    {'trigger': 'reopen', 'source': 'withdrawn', 'dest': 'draft', 'after': 'save_workflow',
     'conditions': ['has_permission']},

    {'trigger': 'reject_hi', 'source': 'pending_review_hi', 'dest': 'draft', 'after': 'save_workflow',
     'conditions': ['has_permission']},
    {'trigger': 'approve_hi', 'source': 'pending_review_hi', 'dest': 'pending_review_fs',
     'after': 'save_workflow', 'conditions': ['has_permission']},

    {'trigger': 'reject_fs', 'source': 'pending_review_fs', 'dest': 'pending_review_hi',
     'after': 'save_workflow', 'conditions': ['has_permission']},
    {'trigger': 'approve_fs', 'source': 'pending_review_fs', 'dest': 'pending_review_su',
     'after': 'save_workflow', 'conditions': ['has_permission']},

    {'trigger': 'reject_su', 'source': 'pending_review_su', 'dest': 'pending_review_fs',
     'after': 'save_workflow', 'conditions': ['has_permission']},
    {'trigger': 'approve_su', 'source': 'pending_review_su', 'dest': 'closed', 'after': 'save_workflow',
     'conditions': ['has_permission']},
    {'trigger': 'reopen_su', 'source': 'closed', 'dest': 'pending_review_su', 'after': 'save_workflow',
     'conditions': ['has_permission']},

    # {'trigger': '*', 'source': '*', 'dest': '*', 'after': 'save_workflow'},
]

WF_FALLSKJERM_TRANSITIONS_ATTR = {
    # 'set_ready': {'title': 'Set Ready', 'action': 'Set Ready', 'resource': 'approve', 'comment': True},
    'send_to_hi': {'title': 'Send til HI', 'action': 'Send til HI', 'resource': 'approve', 'comment': True,
                   'descr': 'Sendt til HI'},
    'withdraw': {'title': 'Trekk tilbake observasjon', 'action': 'Trekk tilbake', 'resource': 'withdraw',
                 'comment': True, 'descr': 'Trekt tilbake'},
    'reopen': {'title': 'Gjenåpne observasjon', 'action': 'Gjenåpne', 'resource': 'reopen', 'comment': True,
               'descr': 'Gjenåpnet'},
    'reject_hi': {'title': 'Avslå observasjon', 'action': 'Avslå', 'resource': 'reject', 'comment': True,
                  'descr': 'Avslått av HI'},
    'approve_hi': {'title': 'Godkjenn observasjon', 'action': 'Godkjenn', 'resource': 'approve',
                   'comment': True, 'descr': 'Godkjent av HI'},
    'reject_fs': {'title': 'Avslå observasjon', 'action': 'Avslå', 'resource': 'reject', 'comment': True,
                  'descr': 'Avslått av Fagsjef'},
    'approve_fs': {'title': 'Godkjenn observasjon', 'action': 'Godkjenn', 'resource': 'approve',
                   'comment': True, 'descr': 'Godkjent av Fagsjef'},
    'reject_su': {'title': 'Avslå observasjon', 'action': 'Avslå', 'resource': 'reject', 'comment': True,
                  'descr': 'Avslått av SU'},
    'approve_su': {'title': 'Godkjenn observasjon', 'action': 'Godkjenn', 'resource': 'approve',
                   'comment': True, 'descr': 'Godkjent av SU'},
    'reopen_su': {'title': 'Gjenåpne observasjon', 'action': 'Gjenåpne', 'resource': 'reopen', 'comment': True,
                  'descr': 'Gjenåpnet av SU'},
}


class ObservationWorkflow(Machine):
    """ For further work, should use https://github.com/einarhuseby/transitions instead of https://github.com/tyarkoni/transitions
    This fork will support the requirements in this project and also keep track of origin
    @todo: add https://github.com/einarhuseby/transitions to site-packages
    @todo: pip install git+https://github.com/einarhuseby/transitions
    @todo: state groups -> then you can see if "in review", "is open" etc
    """

    def __init__(self, object_id=None, initial_state=None, user_id=None, comment=None):

        self.user_id = user_id
        # The states
        # states 'name', 'on_enter', 'on_exit'
        self._states = WF_FALLSKJERM_STATES

        self._state_attrs = WF_FALLSKJERM_ATTR

        """ And some transitions between states. We're lazy, so we'll leave out
        the inverse phase transitions (freezing, condensation, etc.).
        name, source, dest

        This is event chaining methods/functions
        Callbacks: after, before
        conditions: is_flammable, is_something

        Apply to all states
        machine.add_transition('to_liquid', '*', 'liquid')

        Linear states:
        machine.add_ordered_transitions()

        machine.next_state()

        WISHLIST:
        states: should also have an extended version, say {'name':'state_name', 'attr': {whatever you like}
        trigger: dict name, title='approve' or a attributes = {} just to hold some attributes (like states)

        conditions: takes arguments (event) like after & before!!
        [ok] permissions: should be a condition maybe? Conditions will always be first (now we send event_data on conditions)
        All: Set callbacks on _all_ transitions (say has_permission etc)
        Automatic transitions: On expiry/date do transition, on tasks complete/review complete

        Review: all approved => approve, one reject => reject

        """

        """
        Workflows also have wathcers, so call them when something happens!
        And all involved ARE watchers
        @todo: Signals implementation with watchers

        """

        """ The transition definition
        """
        self._transitions = WF_FALLSKJERM_TRANSITIONS

        self.action = None
        """ Extra attributes needed for sensible feedback from API to client

        Permission:
        - owner
        - reporter
        - role - hi - in club!
        - group - fsj, su

        How is this related to acl? Well acl will always be set according to the workflow

        To transition - NEED write permissions!


        """
        self._trigger_attrs = WF_FALLSKJERM_TRANSITIONS_ATTR

        """ Make sure to start with a defined state!
        """
        col = app.data.driver.db[RESOURCE_COLLECTION]

        self.db_wf = col.find_one({'_id': ObjectId(object_id)},
                                  {'id': 1, 'workflow': 1, 'acl': 1, 'club': 1, '_etag': 1, '_version': 1, 'owner': 1,
                                   'reporter': 1, 'organization': 1, 'tags': 1, 'acl': 1})

        initial_state = self.db_wf.get('workflow', {}).get('state', None)

        if initial_state == None or initial_state not in self._states:
            self.initial_state = 'draft'
        else:
            self.initial_state = initial_state

        # Set defaults from 
        self.hi = self.db_wf.get('organization', {}).get('hi', None)
        self.reporter = self.db_wf.get('reporter', None)
        self.owner = self.db_wf.get('owner', None)
        self.club = self.db_wf.get('club', None)
        self.acl_hi = ACL_FALLSKJERM_HI.copy()
        self.acl_hi['club'] = self.club
        self.acl = self.db_wf.get('acl', {})

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
        if len([i for i in app.globals['acl'].get('roles', []) if i in self.acl['execute']['roles']]) > 0 \
                or app.globals['user_id'] in self.acl['execute']['users']:
            return True

        return False

        # return acl_has_permission(self.db_wf['_id'], 'execute', 'observations')

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

        acl = self.db_wf.get('acl')
        club = self.db_wf.get('club')
        reporter = self.db_wf.get('reporter')
        owner = self.db_wf.get('owner')
        reporter = self.db_wf.get('reporter')

        if self.state == 'draft':
            """Only owner can do stuff?"""

            acl['read']['users'] += [reporter]
            acl['write']['users'] += [reporter]
            acl['execute']['users'] = [reporter]

            acl['read']['roles'] += [self.acl_hi]
            acl['write']['roles'] = []
            acl['execute']['roles'] = []


        elif self.state == 'withdrawn':
            """ Only owner! """
            acl['write']['users'] = []
            acl['read']['users'] = [reporter]
            acl['execute']['users'] = [reporter]

            acl['write']['groups'] = []
            acl['read']['groups'] = []
            acl['execute']['groups'] = []

            acl['write']['roles'] = []
            acl['read']['roles'] = []
            acl['execute']['roles'] = []


        elif self.state == 'pending_review_hi':
            """ Owner, reporter read, fsj read, hi read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['write']['roles'] = [self.acl_hi]
            acl['read']['roles'] = [self.acl_hi, ACL_FALLSKJERM_FSJ]
            acl['execute']['roles'] = [self.acl_hi]

        elif self.state == 'pending_review_fs':
            """ Owner, reporter, hi read, fsj read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['write']['roles'] = [ACL_FALLSKJERM_FSJ]
            acl['read']['roles'] = [self.acl_hi, ACL_FALLSKJERM_FSJ, ACL_FALLSKJERM_SU]
            acl['execute']['roles'] = [ACL_FALLSKJERM_FSJ]

        elif self.state == 'pending_review_su':
            """ Owner, reporter, hi, fs read, su read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['read']['roles'] = [self.acl_hi, ACL_FALLSKJERM_FSJ]
            acl['write']['roles'] = []
            acl['execute']['roles'] = [ACL_FALLSKJERM_SU]

        elif self.state == 'closed':
            """ everybody read, su execute """

            # acl['read']['users'] = [] #Should let users still see??
            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['read']['roles'] = [ACL_CLOSED_ALL]
            acl['write']['roles'] = []
            acl['execute']['roles'] = [ACL_FALLSKJERM_SU]

            # Fjernet hele f fallskjermnorge her! Kanskje egen klubb bare?
            self.notification(acl['read']['users'] + acl['execute']['users'] + acl['write']['users'],
                              acl['write']['groups'] + acl['execute']['groups'],
                              acl['read']['roles'] + acl['write']['roles'] + acl['execute']['roles'])

        # Sanity - should really do list comprehension...
        acl['read']['users'] = list(set(acl['read']['users']))
        acl['write']['users'] = list(set(acl['write']['users']))
        acl['execute']['users'] = list(set(acl['execute']['users']))

        acl['read']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['read']['roles'])]
        acl['write']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['write']['roles'])]
        acl['execute']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['execute']['roles'])]

        if self.state != 'closed':
            self.notification(acl['read']['users'] + acl['execute']['users'] + acl['write']['users'],
                              acl['read']['roles'] + acl['write']['roles'] + acl['execute']['roles'])

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

        if self._trigger_attrs.get(event.event.name).get('comment'):
            new.get('workflow').update({'comment': self.comment})

        new['acl'] = self.set_acl()

        # Should really supply the e-tag here, will work! , '_etag': _etag
        # Can also use test_client to do this but it's rubbish or?
        # This will ignore the readonly field skip_validation AND you do not need another domain file for it!!
        result = patch_internal(RESOURCE_COLLECTION, payload=new,
                                concurrency_check=False,
                                skip_validation=True,
                                **{'_id': "%s" % _id, '_etag': "%s" % _etag})
        # test_client().post('/add', data = {'input1': 'a'}}
        # app.test_client().patch('/observations/%s' % _id, data=new, headers=[('If-Match', _etag)])

        # if self.state != self.initial_state:

        if result:
            return True

        return False

    def notification(self, users=[], groups=[], roles=[]):
        """ A wrapper around notifications
        """
        return

        mail = Email()

        """
        recepients = self.helper.get_melwin_users_email(
            self.helper.collect_users(users=users, roles=roles, groups=groups))
        """
        recepients = [{'name': 'Einar Huseby', 'email': 'einar.huseby@gmail.com', 'id': 301041}]
        message = {}

        subject = 'Observasjon #%s %s' % (int(self.db_wf.get('id')), self._trigger_attrs[self.action]['descr'])

        message.update({'observation_id': self.db_wf['id']})
        message.update({'action_by': self.helper.get_user_name(app.globals['user_id'])})
        message.update({'action': self._trigger_attrs[self.action]['descr']})
        message.update({'title': '%s' % ' '.join(self.db_wf.get('tags'))})
        message.update({'wf_from': self._state_attrs[self.initial_state]['description']})
        message.update({'wf_to': self._state_attrs[self.state]['description']})
        message.update({'club': self.helper.get_melwin_club_name(self.db_wf.get('club'))})
        message.update({'date': datetime.today().strftime('%Y-%m-%d %H:%M')})
        message.update({'url': 'app/obs/#!/observation/report/%i\n' % int(self.db_wf.get('id'))})
        message.update({'url_root': request.url_root})
        message.update({'comment': self.comment})
        message.update({'context': 'transition'})

        mail.add_message_html(message, 'ors')
        mail.add_message_plain(message, 'ors')

        mail.send(recepients, subject, prefix='ORS')
