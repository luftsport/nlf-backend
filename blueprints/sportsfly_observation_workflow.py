"""
    Observation Workflow Controller
    ===============================
    
    Model: ext.workflows.observation.ObservationWorkflow
    
    @todo: Signals on change signal to communications to dispatch an update to the watchers
           http://stackoverflow.com/questions/16163139/catch-signals-in-flask-blueprint

"""

from flask import g, Blueprint  # , current_app as app, request, Response, abort, jsonify, make_response
import base64

from ext.workflows.sportsfly_observations import ObservationWorkflow

# Need custom decorators
from ext.app.decorators import *
from ext.app.eve_helper import eve_response

OrsWorkflow = Blueprint('Sportsfly Observation Workflow', __name__, )

RESOURCE_COLLECTION = 'sportsfly_observations'


@OrsWorkflow.route("/<objectid:observation_id>", methods=['GET'])
@OrsWorkflow.route("/<objectid:observation_id>/state", methods=['GET'])
@require_token()
def state(observation_id):
    """ Get current state, actions, transitions and permissions
    """
    # No need for user_id, ObservatoinWorkflow already has that!

    wf = ObservationWorkflow(object_id=observation_id, user_id=g.user_id)

    return eve_response(wf.get_current_state(), 200)

@OrsWorkflow.route("/<objectid:observation_id>/mapping", methods=['GET'])
@require_token()
def mapping(observation_id):
    """ Get mapping for observation workflow
    """
    wf = ObservationWorkflow(object_id=observation_id, user_id=g.user_id)

    return eve_response(wf.get_trigger_attrs(), 200)

@OrsWorkflow.route("/<objectid:observation_id>/audit", methods=['GET'])
@require_token()
def audit(observation_id):
    """ Get audit trail for observation
    """
    wf = ObservationWorkflow(object_id=observation_id, user_id=g.user_id)

    return eve_response(wf.get_audit(), 200)


@OrsWorkflow.route("/legacy/todo", methods=['GET'])
@require_token()
def get_observations():
    """ Get a number of observations which you can execute
        @todo add max_results from GET
    """

    max_results = request.args.get('max_results', 10, type=int)
    page = request.args.get('page', 1, type=int)
    sort_tmp = request.args.get('sort', '_updated', type=str)

    sort = {}

    if sort_tmp[0] == '-':
        sort['field'] = sort_tmp[1:]
        sort['direction'] = -1
    else:
        sort['field'] = sort_tmp
        sort['direction'] = 1

    col = app.data.driver.db[RESOURCE_COLLECTION]
    # db.companies.find().skip(NUMBER_OF_ITEMS * (PAGE_NUMBER - 1)).limit(NUMBER_OF_ITEMS )
    cursor = col.find({'$and': [{'workflow.state': {'$nin': ['closed', 'withdrawn']}},
                                {'$or': [{'acl.execute.users': {'$in': [g.user_id]}},
                                         {'acl.execute.roles': {'$in': g.acl.get('roles', [])}}]}]})

    total_items = cursor.count()

    # _items = list(cursor.sort(sort['field'], sort['direction']).skip(max_results * (page - 1)).limit(max_results))
    _items = list(cursor.sort('id', 1).skip(max_results * (page - 1)).limit(max_results))

    """
    #hateos
    _links = {"self": {"title": "observations/todo", "href": "observations/todo?max_results=%i&page=%i" % (max_results, page),
                       "next": {},
                       "previous": {},
                       "last": {},
                       "first": {},
                       "parent": {}}}
    """
    _meta = {'page': page, 'max_results': max_results, 'total': total_items}
    result = {'_items': _items, '_meta': _meta}
    # return Response(json.dumps(result, default=json_util.default), mimetype='application/json')
    return eve_response(result, 200)


@OrsWorkflow.route(
    '/<objectid:observation_id>/<regex("(approve|reject|withdraw|reopen|ors|ftu|fsj|oou|tku|operativ)"):action>',
    methods=['POST'])
@require_token()
def transition(observation_id, action):
    """
    Perform action on observation
    reject, approve, reopen, withdraw
    request.form.get 
    request.args.get ?q=tal
    @todo: include comment in post!
    @todo: check permissions here??
    """

    comment = None
    try:
        args = request.get_json()  # use force=True to do anyway!
        comment = args.get('comment', '')
    except:
        # Could try form etc
        pass

    # Instantiate with observation_id and current user (user is from g.user_id
    wf = ObservationWorkflow(object_id=observation_id, user_id=g.user_id, comment=comment)

    # Let draft descide to not process in club
    if wf.initial_state == 'draft' and action == 'approve':
        wf.wf_settings['do_not_process_in_club'] = args.get('do_not_process_in_club', False)

    # Let OBSREG descide if not public on close
    if wf.initial_state == 'pending_review_ors':
        wf.wf_settings['do_not_publish'] = args.get('do_not_publish', False)

    # Now just do a

    if wf.get_resource_mapping().get(action, False):
        # result = wf.call(get_actions2().get(action)) #getattr(ObservationWorkflow, wf.get_actions2().get(action))()

        # This is actually safe!
        result = eval('wf.' + wf.get_resource_mapping().get(action) + '()')

        # Change owner signal
        # signal_change_owner.send(app,response=response)

        return eve_response(wf.state, 200)

    return eve_abort(500, 'Error in transitioning observation in workflow')


@OrsWorkflow.route("/<objectid:observation_id>/graph/<string:state>", methods=['GET'])
@require_token()
def graphit(observation_id, state):
    from ext.workflows.sportsfly_observations import WF_SPORTSFLY_STATES, WF_SPORTSFLY_TRANSITIONS
    if state in WF_SPORTSFLY_STATES:
        wf = Dummy()
        import io
        from transitions.extensions import GraphMachine as Machine

        machine = Machine(model=wf,
                          states=WF_SPORTSFLY_STATES,
                          transitions=WF_SPORTSFLY_TRANSITIONS,
                          initial=state,
                          title='Workflow graph')
        stream = io.BytesIO()
        wf.get_graph().draw(stream, prog='dot', format='png')
        # response = make_response(stream.getvalue())
        # response.mimetype = 'image/png'
        # return response
        return eve_response({'graph': base64.b64encode(stream.getvalue())}, 200)


@OrsWorkflow.route("/<objectid:observation_id>/tasks", methods=['GET'])
@require_token()
def tasks(observation_id):
    """
    Get tasks for observation
    
    Not implemented yet, should either be integrated in workflow or as a seperate blueprint?
    
    Most likely this will make for another transition where state is 'waiting for tasks to complete'
    """
    # wf = ObservationWorkflow(object_id=observation_id, user_id=g.user_id)

    raise NotImplemented


class Dummy(object):
    pass
