WF_HPS_STATES = [
    'draft',
    'pending_review_fs',
    'pending_review_obsreg',
    'pending_review_fagutvalg',
    'closed',
    'withdrawn'
]

WF_HPS_ATTR = {
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
    'closed': {
        'title': 'Lukket',
        'description': 'Observasjonen er lukket'
    },
    'withdrawn': {
        'title': 'Trukket',
        'description': 'Observasjonen er trukket tilbake'
    }
}
WF_HPS_TRANSITIONS = [
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
    # Obsreg
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
    {
        'trigger': 'reopen_obsreg',
        'source': 'closed',
        'dest': 'pending_review_obsreg',
        'after': 'save_workflow',
        'conditions': ['has_permission']
    },

]

WF_HPS_TRANSITIONS_ATTR = {
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
        'resource': 'fagsjef',
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
        'resource': 'fagutvalg',
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

}
from ext.workflows.observation_workflow import ObservationWorkflow
from ext.scf import (
    ACL_CLOSED_ALL_LIST,
    ACL_HPS_ORS as ACL_HPS_OBSREG,
    ACL_HPS_FSJ,
    ACL_HPS_CLOSED,
    ACL_HPS_SU_LEDER as ACL_HPS_FAGUTVALG,
    # ACL_HPS_SU_MEDLEM
)


def get_acl_init(person_id, discipline_id):
    acl = {
        'read': {
            'users': [person_id],
            'roles': [ACL_HPS_OBSREG]
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


class HpsObservationWorkflow(ObservationWorkflow):

    def __init__(self, object_id, user_id, activity='hps', initial_state=None, comment=None):

        super().__init__(
            object_id=object_id,
            user_id=user_id,
            activity=activity,
            states=WF_HPS_STATES,
            state_attrs=WF_HPS_ATTR,
            transitions=WF_HPS_TRANSITIONS,
            transitions_attrs=WF_HPS_TRANSITIONS_ATTR,
            initial_state=initial_state,
            comment=comment)

    def set_acl(self):

        """Use self.initial_state as from state!"""

        acl = self.db_wf.get('acl', {})
        reporter = self.db_wf.get('reporter')

        if self.state == 'draft':
            """Only owner can do stuff?"""

            acl['read']['users'] += [reporter]
            acl['write']['users'] = [reporter]
            acl['execute']['users'] = [reporter]

            acl['read']['roles'] += [ACL_HPS_OBSREG]
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
                acl['read']['roles'] = [ACL_HPS_OBSREG]
            else:
                acl['read']['roles'] += [ACL_HPS_OBSREG]
            acl['write']['roles'] = [ACL_HPS_OBSREG]
            acl['execute']['roles'] = [ACL_HPS_OBSREG]

        elif self.state == 'pending_review_fs':
            """ Owner, reporter, hi read, fsj read, write, execute """

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['read']['roles'] += [ACL_HPS_FSJ]
            acl['write']['roles'] = [ACL_HPS_FSJ]
            acl['execute']['roles'] = [ACL_HPS_FSJ]

        elif self.state == 'pending_review_fagutvalg':

            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['read']['roles'] += [ACL_HPS_FAGUTVALG]
            acl['write']['roles'] = [ACL_HPS_FAGUTVALG]
            acl['execute']['roles'] = [ACL_HPS_FAGUTVALG]


        elif self.state == 'closed':
            """ everybody read, su execute """

            # acl['read']['users'] = [] #Should let users still see??
            acl['write']['users'] = []
            acl['execute']['users'] = []

            acl['read']['roles'] += ACL_CLOSED_ALL_LIST
            acl['write']['roles'] = []
            acl['execute']['roles'] = [ACL_HPS_OBSREG]

        # Sanity - should really do list comprehension...
        acl['read']['users'] = list(set(acl['read']['users']))
        acl['write']['users'] = list(set(acl['write']['users']))
        acl['execute']['users'] = list(set(acl['execute']['users']))

        acl['read']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['read']['roles'])]
        acl['write']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['write']['roles'])]
        acl['execute']['roles'] = [dict(y) for y in set(tuple(x.items()) for x in acl['execute']['roles'])]

        return acl
