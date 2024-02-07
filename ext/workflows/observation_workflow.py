from transitions import Machine

from flask import g, current_app as app, request
from bson.objectid import ObjectId

from eve.methods.patch import patch_internal

from datetime import datetime, timedelta

import re

from ext.auth.acl import has_permission as acl_has_permission
from ext.notifications.notifications import get_recepients, get_recepients_from_roles, get_org_name_text, \
    get_person_name_text
from ext.notifications.email import Email  # , Sms
from ext.scf import ACL_CLOSED_ALL_LIST

from ext.app.notifications import ors_workflow
from ext.auth.acl import parse_acl_flat
from ext.scf import HOUSEKEEPING_USER_ID

import abc


def get_wf_init(person_id, activity):
    utc = datetime.utcnow()

    return {'name': f'{activity}_observations_workflow',
            'comment': 'Initialized workflow',
            'state': 'draft',
            'last_transition': utc,
            'expires': utc + timedelta(days=7),
            'audit': [{'a': 'init',
                       'r': 'init',
                       'u': person_id,
                       's': None,
                       'd': 'draft',
                       'v': 1,
                       't': utc,
                       'c': 'Initialized workflow'}]
            }


class ObservationWorkflow(Machine):
    """ For further work, should use https://github.com/einarhuseby/transitions instead of https://github.com/tyarkoni/transitions
    This fork will support the requirements in this project and also keep track of origin
    @todo: add https://github.com/einarhuseby/transitions to site-packages
    @todo: pip install git+https://github.com/einarhuseby/transitions
    RESOURCE_COLLECTION = 'fallskjerm_observations'

    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, object_id, user_id, activity, states, state_attrs, transitions, transitions_attrs,
                 initial_state=None, comment=None):

        self.activity = activity
        self.user_id = user_id
        # The states
        # states 'name', 'on_enter', 'on_exit'
        self._states = states

        self._state_attrs = state_attrs

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
        Workflows also have watchers, so call them when something happens!
        And all involved ARE watchers
        @todo: Signals implementation with watchers

        """

        """ The transition definition
        """
        self._transitions = transitions

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
        self._trigger_attrs = transitions_attrs

        """ Make sure to start with a defined state!
        """
        col = app.data.driver.db[f'{self.activity}_observations']

        self.db_wf = col.find_one({'_id': ObjectId(object_id)},
                                  {'id': 1, 'workflow': 1, 'acl': 1, 'club': 1, 'discipline': 1, '_etag': 1,
                                   '_version': 1, 'owner': 1,
                                   'reporter': 1, 'organization': 1, 'tags': 1})

        initial_state = self.db_wf.get('workflow', {}).get('state', None)

        if initial_state == None or initial_state not in self._states:
            self.initial_state = 'draft'
        else:
            self.initial_state = initial_state

        # Set defaults
        self.reporter = self.db_wf.get('reporter', None)
        self.owner = self.db_wf.get('owner', None)
        self.club = self.db_wf.get('club', None)
        self.discipline = self.db_wf.get('discipline', None)

        #self.acl_hi = ACL_FALLSKJERM_HI.copy()
        #self.acl_hi['org'] = self.discipline

        self.initial_acl = self.db_wf.get('acl', {}).copy()

        self.comment = '' if comment is None else '{}'.format(comment).strip()

        super().__init__(self,
                         states=self._states,
                         send_event=True,
                         transitions=self._transitions,
                         initial=self.initial_state)

        app.logger.info('Initial state: {}'.format(self.initial_state))
        app.logger.info('Self state: {}'.format(self.state))

    def get_actions(self):

        app.logger.info('WF: Self state is: {}'.format(self.state))
        events = []
        for transition in self._transitions:
            app.logger.info('WF: transition iter: {}'.format(transition))
            if self.state == transition['source']:
                app.logger.info(
                    'WF: self state is in transition source: {} {} {}'.format(self.state, transition['source'],
                                                                              transition['trigger']))
                events.append(transition['trigger'])

        return events

    def get_resource_mapping(self):
        """ This will return a dict containing a mapping of resource => trigger
        Example: {'approve': 'approval_from_someone'}
        resource should be utilised in the endpoint/resource and trigger is the callee trigger method in the workflow
        """
        events = {}
        for transition in self._transitions:
            if self.state == transition.get('source', None):
                events.update({self._trigger_attrs.get(transition['trigger']).get('resource'): transition['trigger']})

        return events

    def get_resources(self):

        resources = []

        for event in self.get_actions():
            tmp = self._trigger_attrs.get(event)
            try:
                tmp['permission'] = self.has_permission()
            except Exception as e:
                app.logger.exception('Error in get_resources')

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

    def has_permission(self, event=None):
        """ No events sendt by conditions...
        if event.kwargs.get('user_id', 0) in self.trigger_permissions:
            return True
        return False
        check if in execute!
        """

        # Always grant
        if self.user_id == HOUSEKEEPING_USER_ID:
            return True
        try:
            if len([i for i in g.acl.get('roles', []) if i in self.initial_acl['execute']['roles']]) > 0 \
                    or g.user_id in self.initial_acl['execute']['users']:
                return True
        except Exception as e:
            pass

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

    @abc.abstractmethod
    def set_acl(self):
        raise NotImplemented

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
        new['owner'] = g.user_id

        if self._trigger_attrs.get(event.event.name).get('comment'):
            new.get('workflow').update({'comment': self.comment})

        new['acl'] = self.set_acl()

        # Should really supply the e-tag here, will work! , '_etag': _etag
        # Can also use test_client to do this but it's rubbish or?
        # This will ignore the readonly field skip_validation AND you do not need another domain file for it!!
        response, last_modified, etag, status = patch_internal(f'{self.activity}_observations',
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
            action = self._trigger_attrs[self.action]['resource']

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
            event_from=f'{self.activity}_observations',
            event_from_id=self.db_wf['_id'],
            ors_id=self.db_wf['id'],
            ors_tags=self.db_wf.get('tags', []),
            org_id=self.db_wf.get('discipline'),
            action=action,  # WF_FALLSKJERM_TRANSITIONS_ATTR[action]['action'],
            source=self.initial_state,  # self._state_attrs[self.initial_state]['description'], #
            destination=self.state,  # self._state_attrs[self.state]['description'], #
            comment=self.comment,
            context=context
        )
