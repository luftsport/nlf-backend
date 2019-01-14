"""

Init for the seperated applications and including those into a Domain

@author: Einar Huseby <einar.huseby@gmail.com>

"""

# Import settings files

# User data (avatar, settings, acls etc)
import users, users_auth
import acl_groups, acl_roles, users_acl

# FALLSKJERM
import f_observations
import g_observations
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
import test

# LEGACY
import legacy_melwin_clubs, legacy_melwin_licenses, legacy_melwin_membership, legacy_melwin_users
import legacy_licenses
import legacy_clubs

# Build the Domain to be presented
DOMAIN = {

    # Users
    "users": users.definition,
    "users_acl": users_acl.definition,
    "users_auth": users_auth.definition,

    # ACL
    "acl_groups": acl_groups.definition,
    "acl_roles": acl_roles.definition,

    # Fallskjerm
    "f_observations": f_observations.definition,
    "f_observations_agg": test.definition,

    # Motor
    "g_observations": g_observations.definition,

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
    "tags": tags.definition,

    # Development
    "dev": dev.definition,

    # Help system
    "help": help.definition,

}
