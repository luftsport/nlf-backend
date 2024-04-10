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
from blueprints.sportsfly_observation_workflow import OrsWorkflow as SportsflyOrsWF
from blueprints.seilfly_observation_workflow import OrsWorkflow as SeilflyOrsWF
from blueprints.modellfly_observation_workflow import OrsWorkflow as ModellflyOrsWF

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
from blueprints.content import Content
# Membership integration blueprint
from blueprints.lungo import Lungo
from blueprints.e5x import E5X
from blueprints.heartbeat import Heartbeat
from blueprints.ors import UserORS
from blueprints.housekeeping import Housekeeping


# Custom url mappings (for flask)
from ext.app.url_maps import ObjectIDConverter, RegexConverter

# Custom auth extensions
from ext.auth.tokenauth import TokenAuth

# From notfication
import ext.hooks.notifications as notifications

# Verify startup inside virtualenv
def in_virtualenv():
    def get_base_prefix_compat():
        """Get base/real prefix, or sys.prefix if there is none."""
        return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

    """Support different python versions"""
    if get_base_prefix_compat() != sys.prefix:
        return True
    elif hasattr(sys, 'real_prefix') is True:
        return True

    return False


if not in_virtualenv():
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

# OBSREG NEEDS TO??
app.register_blueprint(FallskjermOrsWF, url_prefix="%s/fallskjerm/observations/workflow" % app.globals.get('prefix'))
app.register_blueprint(MotorflyOrsWF, url_prefix="%s/motorfly/observations/workflow" % app.globals.get('prefix'))
app.register_blueprint(SportsflyOrsWF, url_prefix="%s/sportsfly/observations/workflow" % app.globals.get('prefix'))
app.register_blueprint(SeilflyOrsWF, url_prefix="%s/seilfly/observations/workflow" % app.globals.get('prefix'))
app.register_blueprint(ModellflyOrsWF, url_prefix="%s/modellfly/observations/workflow" % app.globals.get('prefix'))

app.register_blueprint(OrsWatchers, url_prefix="%s/fallskjerm/observations/watchers" % app.globals.get('prefix'))

app.register_blueprint(Locations, url_prefix="%s/locations" % app.globals.get('prefix'))
app.register_blueprint(Tags, url_prefix="%s/tags" % app.globals.get('prefix'))
app.register_blueprint(UserORS, url_prefix="%s/users/observations" % app.globals.get('prefix'))

# app.register_blueprint(OrsShare, url_prefix="%s/fallskjerm/observations/share" % app.globals.get('prefix'))

app.register_blueprint(Notifications, url_prefix="%s/notifications/bin" % app.globals.get('prefix'))

app.register_blueprint(Weather, url_prefix="%s/weather" % app.globals.get('prefix'))
app.register_blueprint(Info, url_prefix="%s/info" % app.globals.get('prefix'))
app.register_blueprint(Files, url_prefix="%s/download" % app.globals.get('prefix'))

app.register_blueprint(Content, url_prefix="%s/content" % app.globals.get('prefix'))

# Membership api blueprint
app.register_blueprint(Lungo, url_prefix="%s/integration" % app.globals.get('prefix'))

app.register_blueprint(E5X, url_prefix="%s/e5x" % app.globals.get('prefix'))

# Heartbeat
app.register_blueprint(Heartbeat, url_prefix="%s/heartbeat" % app.globals.get('prefix'))

# Housekeeping
app.register_blueprint(Housekeeping, url_prefix="%s/housekeeping" % app.globals.get('prefix'))
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


# ##############
# FALLSKJERM OBSREG
#
# POST/DB Insert
app.on_insert_fallskjerm_observations += hook.fallskjerm.ors_before_insert
app.on_inserted_fallskjerm_observations += hook.fallskjerm.ors_after_inserted
# BEFORE GET
app.on_pre_GET_fallskjerm_observations += hook.fallskjerm.ors_before_get
# Get own
app.on_pre_GET_fallskjerm_observations_user += hook.fallskjerm.ors_before_get_user
# Get others
app.on_pre_GET_fallskjerm_observations_todo += hook.fallskjerm.ors_before_get_todo
# AFTER FETCHED (GET)
app.on_fetched_resource_fallskjerm_observations += hook.fallskjerm.ors_after_fetched_list
app.on_fetched_item_fallskjerm_observations += hook.fallskjerm.ors_after_fetched
app.on_fetched_diffs_fallskjerm_observations += hook.fallskjerm.ors_after_fetched_diffs
app.on_fetched_item_fallskjerm_observations_todo += hook.fallskjerm.ors_after_fetched
# BEFORE PATCH/PUT
app.on_pre_PATCH_fallskjerm_observations += hook.fallskjerm.ors_before_patch
# AFTER update db layer
app.on_updated_fallskjerm_observations += hook.fallskjerm.ors_after_update
# Aggregations
app.before_aggregation += hook.fallskjerm.on_aggregate
# ################
# MODELLFLY OBSREG
#
app.on_insert_modellfly_observations += hook.modellfly.ors_before_insert
app.on_inserted_modellfly_observations += hook.modellfly.ors_after_inserted
# BEFORE GET
app.on_pre_GET_modellfly_observations += hook.modellfly.ors_before_get
app.on_pre_GET_modellfly_observations_user += hook.modellfly.ors_before_get_user
app.on_pre_GET_modellfly_observations_todo += hook.modellfly.ors_before_get_todo
# AFTER FETCHED (GET)
app.on_fetched_resource_modellfly_observations += hook.modellfly.ors_after_fetched_list
app.on_fetched_item_modellfly_observations += hook.modellfly.ors_after_fetched
app.on_fetched_diffs_modellfly_observations += hook.modellfly.ors_after_fetched_diffs
app.on_fetched_item_modellfly_observations_todo += hook.modellfly.ors_after_fetched
# BEFORE PATCH/PUT
app.on_pre_PATCH_modellfly_observations += hook.modellfly.ors_before_patch
# BEFORE update db layer
# app.on_update_modellfly_observations += hook.modellfly.ors_before_update
# AFTER update db layer
app.on_updated_modellfly_observations += hook.modellfly.ors_after_update



# ################
# MOTOR OBSREG
#
# BEFORE AND AFTER POST INSERT
app.on_insert_motorfly_observations += hook.motorfly.ors_before_insert
app.on_inserted_motorfly_observations += hook.motorfly.ors_after_inserted
# BEFORE GET
app.on_pre_GET_motorfly_observations += hook.motorfly.ors_before_get
app.on_pre_GET_motorfly_observations_user += hook.motorfly.ors_before_get_user
app.on_pre_GET_motorfly_observations_todo += hook.motorfly.ors_before_get_todo
# AFTER FETCHED (GET)
app.on_fetched_resource_motorfly_observations += hook.motorfly.ors_after_fetched_list
app.on_fetched_item_motorfly_observations += hook.motorfly.ors_after_fetched
app.on_fetched_diffs_motorfly_observations += hook.motorfly.ors_after_fetched_diffs
app.on_fetched_item_motorfly_observations_todo += hook.motorfly.ors_after_fetched
# BEFORE PATCH/PUT
app.on_pre_PATCH_motorfly_observations += hook.motorfly.ors_before_patch
# BEFORE update db layer
app.on_update_motorfly_observations += hook.motorfly.ors_before_update
# AFTER update db layer
app.on_updated_motorfly_observations += hook.motorfly.ors_after_update

# ################
# SEILFLY OBSREG
#
# BEFORE AND AFTER POST INSERT
app.on_insert_seilfly_observations += hook.seilfly.ors_before_insert
app.on_inserted_seilfly_observations += hook.seilfly.ors_after_inserted
# BEFORE GET
app.on_pre_GET_seilfly_observations += hook.seilfly.ors_before_get
app.on_pre_GET_seilfly_observations_user += hook.seilfly.ors_before_get_user
app.on_pre_GET_seilfly_observations_todo += hook.seilfly.ors_before_get_todo
# AFTER FETCHED (GET)
app.on_fetched_resource_seilfly_observations += hook.seilfly.ors_after_fetched_list
app.on_fetched_item_seilfly_observations += hook.seilfly.ors_after_fetched
app.on_fetched_diffs_seilfly_observations += hook.seilfly.ors_after_fetched_diffs
app.on_fetched_item_seilfly_observations_todo += hook.seilfly.ors_after_fetched
# BEFORE PATCH/PUT
app.on_pre_PATCH_seilfly_observations += hook.seilfly.ors_before_patch
# BEFORE update db layer
app.on_update_seilfly_observations += hook.seilfly.ors_before_update
# AFTER update db layer
app.on_updated_seilfly_observations += hook.seilfly.ors_after_update

# ################
# SPORTSFLY OBSREG
#
# BEFORE AND AFTER POST INSERT
app.on_insert_sportsfly_observations += hook.sportsfly.ors_before_insert
app.on_inserted_sportsfly_observations += hook.sportsfly.ors_after_inserted
# BEFORE GET
app.on_pre_GET_sportsfly_observations += hook.sportsfly.ors_before_get
app.on_pre_GET_sportsfly_observations_user += hook.sportsfly.ors_before_get_user
app.on_pre_GET_sportsfly_observations_todo += hook.sportsfly.ors_before_get_todo
# AFTER FETCHED (GET)
app.on_fetched_resource_sportsfly_observations += hook.sportsfly.ors_after_fetched_list
app.on_fetched_item_sportsfly_observations += hook.sportsfly.ors_after_fetched
app.on_fetched_diffs_sportsfly_observations += hook.sportsfly.ors_after_fetched_diffs
app.on_fetched_item_sportsfly_observations_todo += hook.sportsfly.ors_after_fetched
# BEFORE PATCH/PUT
app.on_pre_PATCH_sportsfly_observations += hook.sportsfly.ors_before_patch
# BEFORE update db layer
app.on_update_sportsfly_observations += hook.sportsfly.ors_before_update
# AFTER update db layer
app.on_updated_sportsfly_observations += hook.sportsfly.ors_after_update


###############
# Notifications
app.on_pre_GET_notifications += hook.notifications.before_get

###############
# Aircrafts
app.on_insert_aircrafts += hook.aircrafts.on_insert
app.on_update_aircrafts += hook.aircrafts.on_update


# E5X delete
app.on_pre_DELETE_e5x_attributes += hook.e5x.add_delete_filters
app.on_pre_DELETE_e5x_choices += hook.e5x.add_delete_filters
app.on_pre_DELETE_e5x_tree += hook.e5x.add_delete_filters

# CLUBS, add owner
app.on_insert_legacy_clubs += hook.common.on_insert_set_owner
app.on_update_legacy_clubs += hook.common.on_update_set_owner

#############
# FILES
# AFTER FETCHED (GET)
app.on_fetched_resource_files += hook.files.after_fetched_list
app.on_fetched_item_files += hook.files.after_fetched_item

#############
# CONTENT
app.on_pre_GET_content += hook.content.pre_GET
app.on_pre_PATCH_content += hook.content.pre_PATCH
app.on_pre_DELETE_content += hook.content.pre_DELETE
app.on_insert_content += hook.content.before_insert
app.on_replace_content += hook.content.on_before_replace
app.on_update_content += hook.content.on_before_update

#############
# HELP
app.on_pre_GET_help += hook.help.pre_GET
app.on_pre_PATCH_help += hook.help.pre_PATCH
app.on_pre_DELETE_help += hook.help.pre_DELETE
app.on_insert_help += hook.help.before_insert
app.on_replace_help += hook.help.on_before_replace
app.on_update_help += hook.help.on_before_update


# TEST
def _aggregation(endpoint, pipeline):
    """All aggregation endpoints ends up here"""
    if endpoint == 'notifications_events':
        notifications.before_aggregation(endpoint, pipeline)


# Before any aggregation run this
app.before_aggregation += _aggregation

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

    # Log startup settings from scf
    try:
        from ext.scf import (
            E5X_SEND_TO_LT,
            NOTIFICATION_SEND_EMAIL,
            HOUSEKEEPING,
            HOUSEKEEPING_FIRST_CHORE_DAYS_GRACE,
            HOUSEKEEPING_SECOND_CHORE_DAYS_GRACE,
            HOUSEKEEPING_ACTION_CHORE_DAYS_GRACE
        )
        app.logger.info('[E5X] Send files to LT\t {}'.format(E5X_SEND_TO_LT))
        app.logger.info('[EMAIL] Send email notifications\t {}'.format(NOTIFICATION_SEND_EMAIL))
        app.logger.info('[HOUSEKEEPING] Enabled:\t {}'.format(HOUSEKEEPING))
        if HOUSEKEEPING is True:
            app.logger.info('[HOUSEKEEPING] Days to first warning:\t {}'.format(HOUSEKEEPING_FIRST_CHORE_DAYS_GRACE))
            app.logger.info('[HOUSEKEEPING] Days to second warning:\t {}'.format(HOUSEKEEPING_SECOND_CHORE_DAYS_GRACE))
            app.logger.info('[HOUSEKEEPING] Days to action taken:\t {}'.format(HOUSEKEEPING_ACTION_CHORE_DAYS_GRACE))
    except Exception as e:
        app.logger.exception('Error importing settings from scf.py')

# Run only once
if app.debug and not os.environ.get("WERKZEUG_RUN_MAIN") == "true":


    try:
        import pkg_resources
        print(" App:         %s" % app.config['APP_VERSION'])
        print(" Eve:         %s" % pkg_resources.get_distribution("eve").version)
        print(" Werkzeug:    %s" % pkg_resources.get_distribution("werkzeug").version)
        print(" Cerberus:    %s" % pkg_resources.get_distribution("cerberus").version)
        print(" Flask:       %s" % pkg_resources.get_distribution("flask").version)
        print(" Pymongo:     %s" % pkg_resources.get_distribution("pymongo").version)
        print(" Pillow:      %s" % pkg_resources.get_distribution("Pillow").version)
        print(" Transtions:  %s" % pkg_resources.get_distribution("transitions").version)
        print(" Pytaf:       %s" % pkg_resources.get_distribution("pytaf").version)
        print(" Py Metar:    %s" % pkg_resources.get_distribution("python-metar").version)
        print(" Py YR:       %s" % pkg_resources.get_distribution("python-yr").version)
        print("--------------------------------------------------------------------------------")
    except:
        pass

if __name__ == '__main__':
    app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'])
