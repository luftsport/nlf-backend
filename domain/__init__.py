"""

Init for the seperated applications and including those into a Domain

@author: Einar Huseby <einar.huseby@gmail.com>

"""

# Import settings files

# User data (avatar, settings, acls etc)
import users, users_auth
import acl_groups, acl_roles, users_acl

# FALLSKJERM
import fallskjerm_observations
import motorfly_observations
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
#from notifications import definition as notification_definition
#from notifications import agg_events as notification_agg_events
import app_notifications

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

    # Users
    "users": users.definition,
    "users_acl": users_acl.definition,
    "users_auth": users_auth.definition,

    # Notfication
    "notifications": app_notifications.definition,
    "notifications_events": app_notifications.agg_events,
    # ACL
    "acl_groups": acl_groups.definition,
    "acl_roles": acl_roles.definition,

    # Fallskjerm
    "fallskjerm_observations": fallskjerm_observations.definition,
    "fallskjerm_observations_agg": fallskjerm_observations.aggregate_observation_types,
    "fallskjerm_observations_todo": fallskjerm_observations.workflow_todo,

    # Motor
    "motorfly_observations": motorfly_observations.definition,
    "motorfly_observations_agg": motorfly_observations.aggregate_observation_types,
    "motorfly_observations_todo": motorfly_observations.workflow_todo,

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

    # E5X
    "e5x_attributes": e5x_attributes.definition,
    "e5x_choices": e5x_choices.definition,
    "e5x_choices_count": e5x_choices.agg_count_keys,
    "e5x_tree": e5x_tree.definition,

    # Testing Eve
    "test": test.definition
}
