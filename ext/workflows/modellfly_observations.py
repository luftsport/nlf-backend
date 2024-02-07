WF_MODELLFLY_STATES = [
    'draft',
    'pending_review_fs',
    'pending_review_obsreg',
    'pending_review_klubbleder',
    'pending_review_fagutvalg',
    'closed',
    'withdrawn'
]

WF_MODELLFLY_ATTR = {
    'draft': {
        'title': 'Utkast',
        'description': 'Utkast'
    },
    'pending_review_obsreg': {
        'title': 'Avventer OBSREG',
        'description': 'Avventer vurdering OBSREG koordinator'
    },
    'pending_review_fs': {
        'title': 'Avventer Fagsjef',
        'description': 'Avventer vurdering Fagsjef'
    },
    'pending_review_fagutvalg': {
        'title': 'Avventer Fagutvalg',
        'description': 'Avventer vurdering Fagutvalg'
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
        'trigger': 'send_to_obsreg',
        'source': 'draft',
        'dest': 'pending_review_obsreg',
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
        'trigger': 'reject_obsreg',
        'source': 'pending_review_obsreg',
        'dest': 'draft',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'approve_obsreg',
        'source': 'pending_review_obsreg',
        'dest': 'closed',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    # Fagsjef
    {
        'trigger': 'send_to_fs',
        'source': 'pending_review_obsreg',
        'dest': 'pending_review_fs',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'approve_fs',
        'source': 'pending_review_fs',
        'dest': 'pending_review_obsreg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'reject_fs',
        'source': 'pending_review_fs',
        'dest': 'pending_review_obsreg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    # Fagutvalg
    {
        'trigger': 'send_to_fagutvalg',
        'source': 'pending_review_obsreg',
        'dest': 'pending_review_fagutvalg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'approve_fagutvalg',
        'source': 'pending_review_fagutvalg',
        'dest': 'pending_review_obsreg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'reject_fagutvalg',
        'source': 'pending_review_fagutvalg',
        'dest': 'pending_review_obsreg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    # Leder
    {
        'trigger': 'send_to_klubbleder',
        'source': 'pending_review_obsreg',
        'dest': 'pending_review_klubbleder',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'reject_klubbleder',
        'source': 'pending_review_klubbleder',
        'dest': 'pending_review_obsreg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'approve_klubbleder',
        'source': 'pending_review_klubbleder',
        'dest': 'pending_review_obsreg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },
    {
        'trigger': 'reopen_obsreg',
        'source': 'closed',
        'dest': 'pending_review_obsreg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },

]

WF_MODELLFLY_TRANSITIONS_ATTR = {
    'send_to_obsreg': {
        'title': 'Send til OBSREG Koordinator',
        'action': 'Send OBSREG',
        'resource': 'obsreg',
        'comment': True,
        'descr': 'Sendt til OBSREG Koordinator'
    },
    'approve_obsreg': {
        'title': 'Godkjenn observasjon',
        'action': 'Lukk',
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
    'reopen_obsreg': {
        'title': 'Gjenåpne observasjon',
        'action': 'Gjenåpne',
        'resource': 'reopen',
        'comment': True,
        'descr': 'Gjenåpnet'
    },
    'send_to_fs': {
        'title': 'Send til Fagsjef',
        'action': 'Send til Fagsjef',
        'resource': 'approve',
        'comment': True,
        'descr': 'Sendt til Fagsjef'
    },
    'approve_fs': {
        'title': 'Godkjenn observasjon',
        'action': 'Godkjenn',
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
    'send_to_fagutvalg': {
        'title': 'Send til Fagutvalg',
        'action': 'Send Fagutvalg',
        'resource': 'obsreg',
        'comment': True,
        'descr': 'Sendt til Fagutvalg'
    },
    'approve_fagutvalg': {
        'title': 'Godkjenn observasjon',
        'action': 'Godkjenn',
        'resource': 'approve',
        'comment': True,
        'descr': 'Godkjent av Fagutvalg'
    },
    'reject_fagutvalg': {
        'title': 'Send observasjon tilbake',
        'action': 'Avslå',
        'resource': 'reject',
        'comment': True,
        'descr': 'Sendt tilbake av Fagutvalg'
    },

    'send_to_klubbleder': {
        'title': 'Send til Klubbleder',
        'action': 'Send Klubbleder',
        'resource': 'klubbleder',
        'comment': True,
        'descr': 'Sendt til Klubbleder'
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
from ext.scf import (
    ACL_CLOSED_ALL_LIST,
    ACL_MODELLFLY_KLUBB_LEDER,
    ACL_MODELLFLY_ORS,
    ACL_MODELLFLY_FSJ,
    ACL_MODELLFLY_CLOSED,
    ACL_FALLSKJERM_SU_LEDER_ROLE,
    ACL_FALLSKJERM_SU_MEDLEM_ROLE
)

ACL_MODELLFLY_OBSREG_ROLE = 202656
ACL_FSJ_ROLE = 202659
ACL_KLUBBLEDER_ROLE = 1
ACL_MODELLFLY_OBSREG = {'activity': 236, 'org': 203027, 'role': ACL_MODELLFLY_OBSREG_ROLE}
ACL_KLUBBLEDER = {'activity': 236, 'org': -1, 'role': ACL_KLUBBLEDER_ROLE}
ACL_MODELLFLY_OBSREG = {'activity': 236, 'org': 203027, 'role': ACL_FSJ_ROLE}
ACL_MODELLFLY_FAGUTVALG = {'activity': 236, 'org': 203027, 'role': ACL_FALLSKJERM_SU_MEDLEM_ROLE}


def get_acl_init(person_id, discipline_id):
    acl = {
        'read': {
            'users': [person_id],
            'roles': [ACL_MODELLFLY_OBSREG]
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

            acl['read']['roles'] += [ACL_MODELLFLY_OBSREG]
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


        elif self.state == 'pending_review_obsreg':
            acl['write']['users'] = []
            acl['execute']['users'] = []

            if self.initial_state == 'closed':
                acl['read']['roles'] = [ACL_MODELLFLY_OBSREG]
            else:
                acl['read']['roles'] += [ACL_MODELLFLY_OBSREG]
            acl['write']['roles'] = [ACL_MODELLFLY_OBSREG]
            acl['execute']['roles'] = [ACL_MODELLFLY_OBSREG]

        elif self.state == 'pending_review_fs':
            """ Owner, reporter, hi read, fsj read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['read']['roles'] += [ACL_MODELLFLY_FSJ]
            acl['write']['roles'] = [ACL_MODELLFLY_FSJ]
            acl['execute']['roles'] = [ACL_MODELLFLY_FSJ]

        elif self.state == 'pending_review_fagutvalg':

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['read']['roles'] += [ACL_MODELLFLY_FAGUTVALG]
            acl['write']['roles'] = [ACL_MODELLFLY_FAGUTVALG]
            acl['execute']['roles'] = [ACL_MODELLFLY_FAGUTVALG]

        elif self.state == 'pending_review_klubbleder':
            """ Owner, reporter, hi read, fsj read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []

            klubbleder = ACL_MODELLFLY_KLUBB_LEDER.copy()
            klubbleder['org'] = self.db_wf.get('club')
            acl['read']['roles'] += [klubbleder]
            acl['write']['roles'] = [klubbleder]
            acl['execute']['roles'] = [klubbleder]

        elif self.state == 'closed':
            """ everybody read, su execute """

            # acl['read']['users'] = [] #Should let users still see??
            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['read']['roles'] += ACL_CLOSED_ALL_LIST
            acl['write']['roles'] = []
            acl['execute']['roles'] = [ACL_MODELLFLY_OBSREG]

        # Sanity - should really do list comprehension...
        acl['read']['users'] = list(set(acl['read']['users']))
        acl['write']['users'] = list(set(acl['write']['users']))
        acl['execute']['users'] = list(set(acl['execute']['users']))

        acl['read']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['read']['roles'])]
        acl['write']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['write']['roles'])]
        acl['execute']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['execute']['roles'])]

        return acl
