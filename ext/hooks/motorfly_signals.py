"""
    Signal connections
    ==================
    
    @todo: Need to make functions generic, ie parse resource/endpoint dynamically \
           or via mappings
    
"""

from flask import current_app as app, request, Response, abort

from flask.signals import Namespace

from eve.methods.post import post_internal
from eve.methods.common import oplog_push
from ext.app.eve_helper import eve_abort

from datetime import datetime

import json
from bson.objectid import ObjectId

from ext.auth.helpers import Helpers
from ext.notifications.email import Email  # , Sms

# TIME & DATE - better with arrow only?
import arrow
from datetime import datetime, timedelta
from ext.scf import ACL_FALLSKJERM_HI

_signals = Namespace()

# Define signals
signal_activity_log     = _signals.signal('user-activity-logger')
signal_change_owner     = _signals.signal('change-owner')
signal_change_acl       = _signals.signal('change-acl')
signal_g_init_acl         = _signals.signal('init-g-acl')
signal_motorfly_insert_workflow  = _signals.signal('insert-g-workflow')


@signal_motorfly_insert_workflow.connect
def insert_workflow(dict_app, **extra):
    """ Inserts workflow, wathcers, owner, reporter and custom id on the current resource
    Only when method equals POST
    @todo: need resource->workflow mapping
    @todo: should hook into the given workflow (from mapping?)and retrieve schema OR schema is fixed
    @todo: generic means it can find what to do for each resource (mappings?)
    @TODO: Should really init the state machine in transitions to do this!
    """

    if request.method == 'POST':
        c_app = dict_app.get('app')
        r = dict_app.get('payload')  # request.get_json()
        club = request.get_json().get('club')
        _id = r.get('_id')
        _etag = r.get('_etag')
        _version = r.get('_version')

        utc = datetime.utcnow()
        workflow = {"name": "ObservationWorkflow",
                    "comment": "Initialized workflow",
                    "state": "draft",
                    "last_transition": utc,
                    "expires": utc + timedelta(days=7),
                    "audit": [{'a': "init",
                               'r': "init",
                               'u': c_app.globals.get('user_id'),
                               's': None,
                               'd': "draft",
                               'v': _version,
                               't': utc,
                               'c': "Initialized workflow"}]
                    }

        watchers = [c_app.globals.get('user_id')]

        # Make a integer increment from seq collection
        seq = c_app.data.driver.db['seq']
        seq.update_one({'c': 'g_observations'}, {'$inc': {'i': int(1)}}, True)  # ,fields={'i': 1, '_id': 0},new=True).get('i')
        seq_r = seq.find_one({'c': 'g_observations'}, {'i': 1, '_id': 0})
        number = int(seq_r.get('i'))

        observation = c_app.data.driver.db['g_observations']

        content = {"workflow": workflow,
                   "id": number,
                   "watchers": watchers,
                   "owner": c_app.globals.get('user_id'),
                   "reporter": c_app.globals.get('user_id')
                   }

        result = observation.update_one({'_id': ObjectId(_id), '_etag': _etag}, {"$set": content})

        # NOTIFICATIONS


@signal_g_init_acl.connect
def init_acl(dict_app, **extra):
    """ Set user as read, write and execute!
    Only the current user since this is the POST to DRAFT
    @todo: Investigate wether to keep in workflow or not.
    """

    if request.method == 'POST':

        c_app = dict_app.get('app')
        r = dict_app.get('payload')
        club = request.get_json().get('club')

        _id = r.get('_id')

        obs = c_app.data.driver.db['g_observations']

        # Add hi to the mix!
        #groups = app.data.driver.db['acl_groups']

        # Adds user and hi!
        try:
            acl = {'read': {'users': [app.globals.get('user_id')], 'roles': [ACL_FALLSKJERM_HI]},
                   'write': {'users': [app.globals.get('user_id')], 'roles': []},
                   'execute': {'users': [app.globals.get('user_id')], 'roles': []}
                   }

            test = obs.update_one({'_id': ObjectId(_id)}, {'$set': {'acl': acl}})
            obs.update_one({'_id': ObjectId(_id)}, {'$set': {'organization.hi': app.globals.get('user_id')}})
        except:
            eve_abort(503, 'THe database would not comply with our demands')


@signal_change_owner.connect
def change_owner(c_app, response, **extra):
    """ This solution hooks into after a PATCH request and thus needs the response obj
    The trick is to take the body returned via .get_data() and load it as json
    This ONLY works for Eve specific calls if you do not return the _id included in a json string
    """

    r = json.loads(response.get_data().decode())
    _id = r.get('_id')  # ObjectId(r['_id'])

    try:
        observation = c_app.data.driver.db['fallskjerm_observations']
        u = observation.update_one({'_id': ObjectId(_id)},
                               {"$set": {"owner": c_app.globals.get('user_id')}
                                })
    except:
        pass


@signal_change_acl.connect
def change_obs_acl(c_app, acl, **extra):
    # observation = c_app.data.driver.db['fallskjerm_observations']
    # u = observation.update({})
    pass


@signal_activity_log.connect
def oplog_wrapper(c_app, ref=None, updates=None, action=None, resource=None, **extra):
    """ A simple activity logger wrapping eve's push_oplog
    @todo: Testing and validating of the oplog_push from eve
    @todo: Implement workflow, watchers etc as op (operations)
    """

    raise NotImplementedError

    # def oplog_push(resource, updates, op, id=None):

    if ref == None:
        if request.method == 'POST':  # We do not have any ref before returning, should be sendt!
            pass
        else:
            r = request.get_json()  # Got all _id and _etag
            ref = r.get('_id')

    """ request.endpoint
    A string with 'endpoint|resource' syntax
    """
    if resource == None:
        if request.endpoint:
            resource = request.endpoint.split('|')[0]
        else:
            resource = 'Unknown'

    """ This is NOT tested yet
    @todo: need to replicate the updates dict, which is payload (r?)
    """
    oplog_push(resource=resource, updates=r, op=request.method, id=ref)
