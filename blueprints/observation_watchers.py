"""
    Watchers
    ========
    
    Simple watchers resource
    
    - start and stop watching
    - return a list of watchers (list)
    - if current user is watching (boolean)
    
    @note: Watching uses direct db access, so no new version will 
    
    @todo: add signals on start and stop for audit
    @todo: implement audit (likely through signals)
    @todo: implement updating from workflow?
    @todo: refactor and have all changes in a model, this being the controller hence it can be called from other resources
    
    See signals on http://stackoverflow.com/questions/16163139/catch-signals-in-flask-blueprint
    
    
"""

from flask import g, Blueprint, current_app as app, request, Response, abort, jsonify
from bson import json_util
import json
from bson.objectid import ObjectId


from eve.methods.patch import patch_internal

# Need custom decorators
from ext.app.decorators import *

OrsWatchers = Blueprint('Observation Watchers', __name__, )

@OrsWatchers.route("/<objectid:observation_id>/", methods=['GET'])
@OrsWatchers.route("/<objectid:observation_id>/watchers", methods=['GET'])
@require_token()
def watchers(observation_id):
    
    w = get_watchers(observation_id)
    
    return jsonify(**{'watchers': w})

@OrsWatchers.route("/<objectid:observation_id>/watching", methods=['GET'])
@require_token()
def is_watching(observation_id):
    
    if g.user_id in get_watchers(observation_id):
        return jsonify(**{'watching': True})
    
    return jsonify(**{'watching': False})

@OrsWatchers.route("/<objectid:observation_id>/start", methods=['POST'])
@require_token()
def start(observation_id):
    """ Start watching an observation """
    
    w = get_watchers(observation_id)
    
    if g.user_id not in w:
        new_watchers = []
        new_watchers.append(g.user_id)
        new_watchers.extend(w)
        
        r = update_watchers(observation_id, new_watchers)
        
        if r:
            return jsonify(**{'watching': True})
    
    return jsonify(**{'watching': False})

@OrsWatchers.route("/<objectid:observation_id>/stop", methods=['POST'])
@require_token()
def stop(observation_id):
    
    w = get_watchers(observation_id)
    
    if g.user_id in w:

        w = [x for x in w if x != g.user_id]

        r = update_watchers(observation_id, w)
        
        if r:
            return jsonify(**{'watching': False})
    
    return jsonify(**{'watching': True})

def get_watchers(observation_id):
    
    col = app.data.driver.db['fallskjerm_observations']
    
    r = col.find_one({'_id': ObjectId(observation_id)}, {'watchers': 1})
   
    return r['watchers']

def update_watchers(observation_id, watchers):
    """ Wrapper to keep update segregated """
    
    col = app.data.driver.db['fallskjerm_observations']

    r = col.update({'_id': ObjectId(observation_id)}, {"$set": {"watchers": watchers}})
    
    if r:
        return True
    
    return False
    
    

