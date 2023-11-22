WF_MODELLFLY_STATES = [
    'draft',
    'pending_review_fs',
    'pending_review_obsreg',
    'pending_review_klubbleder',
    'closed',
    'withdrawn'
]

WF_MODELLFLY_ATTR = {
    'draft': {
        'title': 'Utkast',
        'description': 'Utkast'
    },
    'pending_review_fs': {
        'title': 'Avventer Fagsjef',
        'description': 'Avventer vurdering Fagsjef'
    },
    'pending_review_obsreg': {
        'title': 'Avventer OBSREG',
        'description': 'Avventer vurdering OBSREG koordinator'
    },
    'pending_review_klubbleder': {
        'title': 'Avventer Klubbleder',
        'description': 'Avventer vurdering Klubbleder'
    },
    'closed': {
        'title': 'Lukket',
        'description': 'Observasjonen er lukket'
    },
    'withdrawn': {
        'title': 'Trukket',
        'description': 'Observasjonen er trukket tilbake'
    }
}
WF_MODELLFLY_TRANSITIONS = [
    {
        'trigger': 'send_to_fs',
        'source': 'draft',
        'dest': 'pending_review_fs',
        'after': 'save_workflow',
        'conditions': ['has_permission'],
    },
    {
        'trigger': 'withdraw',
        'source': 'draft',
        'dest': 'withdrawn',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'reopen',
        'source': 'withdrawn',
        'dest': 'draft',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },

    {
        'trigger': 'reject_fs',
        'source': 'pending_review_fs',
        'dest': 'draft',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'approve_fs',
        'source': 'pending_review_fs',
        'dest': 'closed',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    # OBSREG
    {
        'trigger': 'approve_fs_obsreg',
        'source': 'pending_review_fs',
        'dest': 'pending_review_obsreg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'approve_obsreg',
        'source': 'pending_review_obsreg',
        'dest': 'pending_review_fs',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'reject_obsreg',
        'source': 'pending_review_obsreg',
        'dest': 'pending_review_fs',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    # Leder
    {
        'trigger': 'approve_fs_klubbleder',
        'source': 'pending_review_fs',
        'dest': 'pending_review_klubbleder',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },

    {
        'trigger': 'reject_klubbleder',
        'source': 'pending_review_klubbleder',
        'dest': 'pending_review_fs',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'approve_klubbleder',
        'source': 'pending_review_klubbleder',
        'dest': 'pending_review_fs',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'reopen_fs',
        'source': 'closed',
        'dest': 'pending_review_fs',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },

]

WF_MODELLFLY_TRANSITIONS_ATTR = {
    'send_to_fs': {
        'title': 'Send til Fagsjef',
        'action': 'Send til Fagsjef',
        'resource': 'approve',
        'comment': True,
        'descr': 'Sendt til Fagsjef'
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
    'reopen_fs': {
        'title': 'Gjenåpne observasjon',
        'action': 'Gjenåpne',
        'resource': 'reopen',
        'comment': True,
        'descr': 'Gjenåpnet'
    },
    'approve_fs': {
        'title': 'Godkjenn observasjon',
        'action': 'Lukk',
        'resource': 'approve',
        'comment': True,
        'descr': 'Godkjent av Fagsjef'
    },
    'reject_fs': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt tilbake av Fagsjef'
    },
    'approve_obsreg': {
        'title': 'Godkjenn observasjon',
        'action': 'Godkjenn',
        'resource': 'approve',
        'comment': True,
        'descr': 'Godkjent av OBSREG koordinator'
    },
    'reject_obsreg': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt tilbake av OBSREG koordinator'
    },
    'approve_klubbleder': {
        'title': 'Godkjenn observasjon',
        'action': 'Godkjenn',
        'resource': 'approve',
        'comment': True,
        'descr': 'Godkjent av Klubbleder'
    },
    'reject_klubbleder': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt tilbake av Klubbleder'
    }

}
from ext.workflows.observation_workflow import ObservationWorkflow
from ext.scf import ACL_CLOSED_ALL_LIST


ACL_MODELLFLY_OBSREG_ROLE = 202656
ACL_MODELLFLY_OBSREG = {'activity': 236, 'org': 203027, 'role': ACL_MODELLFLY_OBSREG_ROLE}
ACL_MODELLFLY_FS = {'activity': 236, 'org': 203027, 'role': ACL_MODELLFLY_OBSREG_ROLE}
ACL_FSJ_ROLE = 202659
ACL_KLUBBLEDER_ROLE = 1
ACL_KLUBBLEDER = {'activity': 236, 'org': -1, 'role': ACL_KLUBBLEDER_ROLE}
ACL_MODELLFLY_FS = {'activity': 236, 'org': 203027, 'role': ACL_FSJ_ROLE}

def get_acl_init(person_id, discipline_id):
    acl = {
        'read': {
            'users': [person_id],
            'roles': [ACL_MODELLFLY_FS]
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

class ModellflyObservationWorkflow(ObservationWorkflow):

    def __init__(self, object_id, user_id, activity='modellfly', initial_state=None, comment=None):

        super().__init__(
                         object_id=object_id,
                         user_id=user_id,
                         activity=activity,
                         states=WF_MODELLFLY_STATES,
                         state_attrs=WF_MODELLFLY_ATTR,
                         transitions=WF_MODELLFLY_TRANSITIONS,
                         transitions_attrs=WF_MODELLFLY_TRANSITIONS_ATTR,
                         initial_state=None,
                         comment=None)

    def set_acl(self):

        """Use self.initial_state as from state!"""

        acl = self.db_wf.get('acl', {})
        reporter = self.db_wf.get('reporter')

        if self.state == 'draft':
            """Only owner can do stuff?"""

            acl['read']['users'] += [reporter]
            acl['write']['users'] = [reporter]
            acl['execute']['users'] = [reporter]

            acl['read']['roles'] += [ACL_MODELLFLY_FS]
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


        elif self.state == 'pending_review_fs':
            """ Owner, reporter read, fsj read, hi read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['write']['roles'] = [ACL_MODELLFLY_FS]
            acl['read']['roles'] += [ACL_MODELLFLY_FS]
            acl['execute']['roles'] = [ACL_MODELLFLY_FS]

        elif self.state == 'pending_review_obsreg':
            """ Owner, reporter, hi read, fsj read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['write']['roles'] = [ACL_MODELLFLY_FS]
            acl['read']['roles'] += [ACL_MODELLFLY_FS, ACL_MODELLFLY_OBSREG]
            acl['execute']['roles'] = [ACL_MODELLFLY_OBSREG]

        elif self.state == 'pending_review_klubbleder':
            """ Owner, reporter, hi read, fsj read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []
            klubbleder = ACL_KLUBBLEDER.copy()
            klubbleder['org'] = self.db_wf.get('club')
            acl['write']['roles'] = [ACL_MODELLFLY_FS]
            acl['read']['roles'] += [ACL_MODELLFLY_FS, ACL_MODELLFLY_OBSREG]
            acl['execute']['roles'] = [ACL_MODELLFLY_OBSREG]

        elif self.state == 'closed':
            """ everybody read, su execute """

            # acl['read']['users'] = [] #Should let users still see??
            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['read']['roles'] += ACL_CLOSED_ALL_LIST
            acl['write']['roles'] = []
            acl['execute']['roles'] = ACL_MODELLFLY_FS

        # Sanity - should really do list comprehension...
        acl['read']['users'] = list(set(acl['read']['users']))
        acl['write']['users'] = list(set(acl['write']['users']))
        acl['execute']['users'] = list(set(acl['execute']['users']))

        acl['read']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['read']['roles'])]
        acl['write']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['write']['roles'])]
        acl['execute']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['execute']['roles'])]

        return acl
