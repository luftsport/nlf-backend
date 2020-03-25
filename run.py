"""
    NLF-backend
    ===========

    @note: Pip stuff as a reminder
    
            Update all packages in one go!
            pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U
            
            Find outdated packages
            pip list --outdated
    
    @note: Run as `nohup python run.py >> nlf.log 2>&1&` NB in virtualenv!
    
    @author:        Einar Huseby
    @copyright:     (c) 2014-2019 Norges Luftsportsforbund
    @license:       GPLV1, see LICENSE for more details.
"""

import os, sys
# from ext.app.custom_eve import CustomEve
from eve import Eve

# We need the json serializer from flask.jsonify (faster than "".json())
# flask.request for custom flask routes (no need for schemas, database or anything else)
from flask import jsonify, request, abort, Response

# Swagger docs
from eve_swagger import swagger

# from ext.app.eve_helper import eve_error_response

# Auth and Authz blueprints
from blueprints.authentication import Authenticate
from blueprints.acl import ACL
# Observation blueprints
from blueprints.fallskjerm_observation_workflow import OrsWorkflow as FallskjermOrsWF
from blueprints.motorfly_observation_workflow import OrsWorkflow as MotorflyOrsWF

from blueprints.observation_watchers import OrsWatchers
from blueprints.observation_share import OrsShare
from blueprints.locations import Locations
# Notifications blueprint
from blueprints.notifications import Notifications
# Misc blueprints
from blueprints.weather import Weather
from blueprints.info import Info
from blueprints.files import Files
from blueprints.tags import Tags
# Membership integration blueprint
from blueprints.lungo import Lungo
from blueprints.e5x import E5X
from blueprints.heartbeat import Heartbeat

# Custom url mappings (for flask)
from ext.app.url_maps import ObjectIDConverter, RegexConverter

# Custom auth extensions
from ext.auth.tokenauth import TokenAuth

# Verify startup inside virtualenv
if not hasattr(sys, 'real_prefix'):
    print("Outside virtualenv, aborting....")
    sys.exit(-1)

# Make sure gunicorn passes settings.py
SETTINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.py')

# Start Eve (and flask)
# Instantiate with custom auth
# app = CustomEve(auth=TokenAuth, settings=SETTINGS_PATH)
# app = Eve(settings=SETTINGS_PATH)
app = Eve(auth=TokenAuth, settings=SETTINGS_PATH)

""" Define global settings
These settings are mirrored from Eve, but should not be!
@todo: use app.config instead
"""
app.globals = {"prefix": "/api/v1"}
app.globals.update({"auth": {}})
app.globals['auth'].update({"auth_collection": "users_auth",
                            "users_collection": "users"})

# Custom url mapping (needed by native flask routes)
app.url_map.converters['objectid'] = ObjectIDConverter
app.url_map.converters['regex'] = RegexConverter

# Register eve-docs blueprint 
# app.register_blueprint(eve_docs,        url_prefix="%s/docs" % app.globals.get('prefix'))
app.register_blueprint(swagger)
# You might want to simply update the eve settings module instead.


# Register custom blueprints
app.register_blueprint(Authenticate, url_prefix="%s/user" % app.globals.get('prefix'))
app.register_blueprint(ACL, url_prefix="%s/acl" % app.globals.get('prefix'))

# ORS NEEDS TO??
app.register_blueprint(FallskjermOrsWF, url_prefix="%s/fallskjerm/observations/workflow" % app.globals.get('prefix'))
app.register_blueprint(MotorflyOrsWF, url_prefix="%s/motorfly/observations/workflow" % app.globals.get('prefix'))

app.register_blueprint(OrsWatchers, url_prefix="%s/fallskjerm/observations/watchers" % app.globals.get('prefix'))

app.register_blueprint(Locations, url_prefix="%s/locations" % app.globals.get('prefix'))
app.register_blueprint(Tags, url_prefix="%s/tags" % app.globals.get('prefix'))
app.register_blueprint(OrsShare, url_prefix="%s/fallskjerm/observations/share" % app.globals.get('prefix'))

app.register_blueprint(Notifications, url_prefix="%s/notifications/bin" % app.globals.get('prefix'))


app.register_blueprint(Weather, url_prefix="%s/weather" % app.globals.get('prefix'))
app.register_blueprint(Info, url_prefix="%s/info" % app.globals.get('prefix'))
app.register_blueprint(Files, url_prefix="%s/download" % app.globals.get('prefix'))

# Membership api blueprint
app.register_blueprint(Lungo, url_prefix="%s/integration" % app.globals.get('prefix'))

app.register_blueprint(E5X, url_prefix="%s/e5x" % app.globals.get('prefix'))

# Heartbeat
app.register_blueprint(Heartbeat, url_prefix="%s/heartbeat" % app.globals.get('prefix'))
"""
    Eve hooks
    ~~~~~~~~~
    
    This are located in ext.hooks package
"""
# Import hooks
import ext.hooks as hook


def dump_request(request):
    try:
        print(app.config['SOURCES'])
    except Exception as e:
        pass


# ORS
# Fallskjerm
# POST
app.on_insert_fallskjerm_observations += hook.fallskjerm.ors_before_insert
# BEFORE GET
app.on_pre_GET_fallskjerm_observations += hook.fallskjerm.before_get
app.on_pre_GET_fallskjerm_observations_todo += hook.fallskjerm.before_get_todo
# AFTER FETCHED (GET)
app.on_fetched_item_fallskjerm_observations += hook.fallskjerm.after_fetched
app.on_fetched_item_fallskjerm_observations_todo += hook.fallskjerm.after_fetched
app.on_fetched_diffs_fallskjerm_observations += hook.fallskjerm.after_fetched_diffs
# BEFORE PATCH/PUT
app.on_pre_PATCH_fallskjerm_observations += hook.fallskjerm.before_patch

## MOTOR
# BEFORE AND AFTER POST INSERT
app.on_insert_motorfly_observations += hook.motorfly.ors_before_insert
app.on_inserted_motorfly_observations += hook.motorfly.ors_after_insert  # no id??
# BEFORE GET
app.on_pre_GET_motorfly_observations += hook.motorfly.before_get
app.on_pre_GET_motorfly_observations_todo += hook.motorfly.before_get_todo
# AFTER FETCHED (GET)
app.on_fetched_item_motorfly_observations += hook.motorfly.after_fetched
app.on_fetched_item_motorfly_observations_todo += hook.motorfly.after_fetched
app.on_fetched_diffs_motorfly_observations += hook.motorfly.after_fetched_diffs
# BEFORE PATCH/PUT
app.on_pre_PATCH_motorfly_observations += hook.motorfly.before_patch

# Aircrafts
app.on_insert_aircrafts += hook.aircrafts.on_insert
app.on_update_aircrafts += hook.aircrafts.on_update

# E5X delete
app.on_pre_DELETE_e5x_attributes += hook.e5x.add_delete_filters
app.on_pre_DELETE_e5x_choices += hook.e5x.add_delete_filters
app.on_pre_DELETE_e5x_tree += hook.e5x.add_delete_filters

# Motor

# app.on_post_POST_g_observations += hook.fallskjerm.after_g_post
# app.on_pre_POST_fallskjerm_observations += dump_request

# app.on_pre_PATCH_fallskjerm_observations += hook.fallskjerm.before_patch

# app.on_post_PATCH_fallskjerm_observations += hook.fallskjerm.after_patch

# app.on_insert_oplog += hook.oplog.before_insert

# app.on_pre_GET_observations += observations_before_get
# app.on_pre_POST_observations += observations_before_post
# app.on_pre_PATCH_observations += observations_before_patch


# app.on_insert += hook.observations.before_post_comments
app.on_insert_f_observation_comments += hook.fallskjerm.before_post_comments

# app.on_post_GET_fallskjerm_observations += hook.observations.after_get
# app.on_fetched_item_fallskjerm_observations += hook.observations.after_fetched


# Help hooks
app.on_insert_help += hook.help.on_insert_items
# app.on_pre_PATCH_help += hook.help.before_patch
# app.on_post_POST_help += hook.help.after_post
# Content hooks
app.on_insert_content += hook.content.before_insert

# CLUBS, add owner
app.on_insert_legacy_clubs += hook.common.on_insert_set_owner
app.on_update_legacy_clubs += hook.common.on_update_set_owner

# App error hooks
@app.errorhandler(401)
def http_401(e):
    return jsonify(error=str(e)), 401
    #  eve_error_response(str(e), 401)


@app.errorhandler(403)
def http_403(e):
    return jsonify(error=str(e)), 403


@app.errorhandler(500)
def http_500(e):
    return jsonify(error=str(e)), 500


@app.errorhandler(501)
def http_501(e):
    # app.logger.exception('Error 501 handler')
    return jsonify(error=str(e)), 501


""" A simple python logger setup
Use app.logger.<level>(<message>) for manual logging
Levels: debug|info|warning|error|critical"""
if 1 == 1 or not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('nlf-backend.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.info('NLF-backend startup on database:\t %s' % app.config['MONGO_DBNAME'].upper())
    app.logger.info('NLF-backend instance:\t %s' % app.config['APP_INSTANCE'].upper())

# Run only once
if app.debug and not os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    import pkg_resources

    print(" App:         %s" % app.config['APP_VERSION'])
    print(" Eve:         %s" % pkg_resources.get_distribution("eve").version)
    print(" Cerberus:    %s" % pkg_resources.get_distribution("cerberus").version)
    print(" Flask:       %s" % pkg_resources.get_distribution("flask").version)
    print(" Pymongo:     %s" % pkg_resources.get_distribution("pymongo").version)
    print(" Pillow:      %s" % pkg_resources.get_distribution("Pillow").version)
    print(" Transtions:  %s" % pkg_resources.get_distribution("transitions").version)
    print(" Pytaf:       %s" % pkg_resources.get_distribution("pytaf").version)
    print(" Py Metar:    %s" % pkg_resources.get_distribution("python-metar").version)
    print(" Py YR:       %s" % pkg_resources.get_distribution("python-yr").version)
    print("--------------------------------------------------------------------------------")

if __name__ == '__main__':
    app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'])
