"""

    Aircrafts hooks:
    ===============

"""
import ext.auth.anonymizer as anon
from ext.auth.acl import get_user_acl_mapping
import ext.app.eve_helper as eve_helper
from ext.app.decorators import *
import json
# import signals from hooks
from ext.hooks.fallskjerm_signals import signal_activity_log, signal_insert_workflow, \
    signal_change_owner, signal_init_acl
from ext.hooks.motorfly_signals import signal_g_init_acl, signal_motorfly_insert_workflow

from ext.scf import ACL_FALLSKJERM_HI, ACL_FALLSKJERM_SU_GROUP, ACL_FALLSKJERM_FSJ
from ext.workflows.fallskjerm_observations import get_wf_init, get_acl_init
from ext.app.seq import increment
from ext.app.lungo import get_person_from_role


def on_insert(items):

    for key, item in enumerate(items):
        items[key]['updated_by'] = int(app.globals.get('user_id'))


def on_update(item, original):
    item['updated_by'] = int(app.globals.get('user_id'))
