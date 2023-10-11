"""

Init for the seperated applications and including those into a Domain

"""

# Import settings files
import app_config

# User data (avatar, settings, acls etc)
import users, users_auth
import acl_groups, acl_roles, users_acl

# FALLSKJERM
import fallskjerm_observations
import fallskjerm_quarter_report

# Modellfly
import modellfly_observations

# MOTORFLY
import motorfly_observations

import seilfly_observations

import sportsfly_observations

# import observation_components
# import observation_comments
# Files - just a test collection
import files
import tags

# Help and content system
import help
import content, content_aggregations

# A custom endpoint for developement flexibility!
import dev

# NOTIFICATIONS
# from notifications import definition as notification_definition
# from notifications import agg_events as notification_agg_events
import app_notifications
import housekeeping

# LEGACY
import legacy_melwin_clubs, legacy_melwin_licenses, legacy_melwin_membership, legacy_melwin_users
import legacy_licenses
import legacy_clubs

# Aircrafts
import aircrafts
# Airports OurAirports
import aip_airports
import aip_frequencies
import aip_runways
import aip_navaids
import aip_countries
import aip_regions
# import openaip_airports
import aip_airspaces

# Geo
import geo_countries
import geo_admin

# E5X
import e5x_attributes, e5x_choices, e5x_tree

# Eve testing
import test

# Build the Domain to be presented
DOMAIN = {
    # App config
    "app_config": app_config.definition,

    # Users
    "users": users.definition,
    "users_acl": users_acl.definition,
    "users_auth": users_auth.definition,

    # Notfication
    "notifications": app_notifications.definition,
    "notifications_events": app_notifications.agg_events,

    # Housekeeping logs
    "housekeeping": housekeeping.definition,

    # Fallskjerm
    "fallskjerm_observations": fallskjerm_observations.definition,
    "fallskjerm_observations_user": fallskjerm_observations.user,
    "fallskjerm_observations_todo": fallskjerm_observations.workflow_todo,
    # Fallskjerm aggregations
    "fallskjerm_observations_aggregate_types": fallskjerm_observations.aggregate_types,
    "fallskjerm_observations_aggregate_types_discipline": fallskjerm_observations.aggregate_types_discipline,
    "fallskjerm_observations_aggregate_states_discipline": fallskjerm_observations.aggregate_states_discipline,
    "fallskjerm_observations_aggregate_avg_ratings_discipline": fallskjerm_observations.aggregate_avg_rating_discipline,
    "fallskjerm_observations_aggregate_avg_ratings": fallskjerm_observations.aggregate_avg_rating,

    # Fallskjerm kvartallstall
    "fallskjerm_quarter_report": fallskjerm_quarter_report.definition,
    "fallskjerm_quarter_report_aggregate_year": fallskjerm_quarter_report.aggregate_year,
    
    # Modell
    "modellfly_observations": modellfly_observations.definition,
    "modellfly_observations_user": modellfly_observations.user,
    "modellfly_observations_todo": modellfly_observations.workflow_todo,
    # Modell aggregations
    "modellfly_observations_aggregate_types": modellfly_observations.aggregate_types,
    "modellfly_observations_aggregate_types_discipline": modellfly_observations.aggregate_types_discipline,
    "modellfly_observations_aggregate_states_discipline": modellfly_observations.aggregate_states_discipline,

    # Motor
    "motorfly_observations": motorfly_observations.definition,
    "motorfly_observations_user": motorfly_observations.user,
    "motorfly_observations_todo": motorfly_observations.workflow_todo,
    # Motor aggregations
    "motorfly_observations_aggregate_types": motorfly_observations.aggregate_types,
    "motorfly_observations_aggregate_types_discipline": motorfly_observations.aggregate_types_discipline,
    "motorfly_observations_aggregate_states_discipline": motorfly_observations.aggregate_states_discipline,

    # Seil
    "seilfly_observations": seilfly_observations.definition,
    "seilfly_observations_user": seilfly_observations.user,
    "seilfly_observations_todo": seilfly_observations.workflow_todo,
    # Seil aggregations
    "seilfly_observations_aggregate_types": seilfly_observations.aggregate_types,
    "seilfly_observations_aggregate_types_discipline": seilfly_observations.aggregate_types_discipline,
    "seilfly_observations_aggregate_states_discipline": seilfly_observations.aggregate_states_discipline,

    # Sportsfly
    "sportsfly_observations": sportsfly_observations.definition,
    "sportsfly_observations_user": sportsfly_observations.user,
    "sportsfly_observations_todo": sportsfly_observations.workflow_todo,
    # Sportsfly aggregations
    "sportsfly_observations_aggregate_types": sportsfly_observations.aggregate_types,
    "sportsfly_observations_aggregate_types_discipline": sportsfly_observations.aggregate_types_discipline,
    "sportsfly_observations_aggregate_states_discipline": sportsfly_observations.aggregate_states_discipline,
    
    # Fallskjerm legacy
    "legacy_licenses": legacy_licenses.definition,
    "legacy_clubs": legacy_clubs.definition,
    "legacy_melwin_licenses": legacy_melwin_licenses.definition,
    "legacy_melwin_membership": legacy_melwin_membership.definition,
    "legacy_melwin_clubs": legacy_melwin_clubs.definition,
    "legacy_melwin_users": legacy_melwin_users.definition,

    # Content
    "content": content.definition,
    "content_aggregate_parents": content_aggregations.parents,
    "content_aggregate_children": content_aggregations.children,
    "content_aggregate_siblings": content_aggregations.siblings,

    # Common
    "files": files.definition,
    "agg_duplicate_files": files.agg_duplicate_files,
    "agg_orphan_files": files.agg_orphan_files,

    # Tags
    "tags": tags.definition,

    # Development
    "dev": dev.definition,

    # Help system
    "help": help.definition,

    # E5X
    "e5x_attributes": e5x_attributes.definition,
    "e5x_choices": e5x_choices.definition,
    "e5x_choices_count": e5x_choices.agg_count_keys,
    "e5x_tree": e5x_tree.definition,

    # @TODO REMOVE
    # Moved to lungo

    # Aircrafts
    "aircrafts": aircrafts.definition,
    "aircrafts_types": aircrafts.agg_count_types,

    # Airports and stuff
    "aip_airports": aip_airports.definition,
    "aip_airspaces": aip_airspaces.definition,
    "aip_frequencies": aip_frequencies.definition,
    "aip_runways": aip_runways.definition,
    "aip_navaids": aip_navaids.definition,
    "aip_countries": aip_countries.definition,
    "aip_regions": aip_regions.definition,
    # "openaip_airports": openaip_airports.definition,

    # Geo
    "geo_countries": geo_countries.definition,
    "geo_admin": geo_admin.definition,
}
