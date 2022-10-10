# encoding: utf-8
"""Custom implementations of auth functions from ckan.logic.auth.get
"""

import logging
import re

from ckan.authz import has_user_permission_for_group_or_org
import ckan.plugins as plugins
import ckan.logic.auth.get as ckanget
import ckan.common as c
import ckan.lib.helpers as h
import ckan.authz as authz
import ckan.logic as logic
from ckan.model.group import Group

LOG = logging.getLogger(__name__)


# xyz_list functions:
# egrep "def ([a-z_]+?_list(_[a-z_]+?)?)\(" ckan/logic/auth/get.py | sort | uniq

def member_roles_list(context, data_dict):
    """Implementation of ckan.logic.auth.get.member_roles_list

    - everyone: disallow
    """
    return {
        'success': False,
        'msg': 'You are not authorized to perform the member_roles_list action.'
    }


@plugins.toolkit.auth_allow_anonymous_access
def organization_list_for_user(context, data_dict):
    """Implementation of ckan.logic.auth.get.organization_list_for_user

    - anonymous: disallow (TODO: temporarily allowed because of CKAN core's missing auth_user_obj bug)
    - all others: standard behaviour
    """
    return ckanget.organization_list_for_user(context, data_dict)


def user_list(context, data_dict):
    """Implementation of ckan.logic.auth.get.user_list

    - everyone: disallow
    """
    return {
        'success': False,
        'msg': 'You are not authorized to perform the user_list action.'
    }


@plugins.toolkit.auth_disallow_anonymous_access
def vocabulary_list(context, data_dict):
    """Implementation of ckan.logic.auth.get.vocabulary_list

    - anonymous: disallow
    - all others: standard behaviour
    """
    return ckanget.vocabulary_list(context, data_dict)


# xyz_show functions:
# egrep "def ([a-z_]+?_show(_[a-z_]+?)?)\(" ckan/logic/auth/get.py | sort | uniq

@plugins.toolkit.auth_allow_anonymous_access
def group_show(context, data_dict):
    """Implementation of ckan.logic.auth.get.group_show

    - anonymous: disallow, except through through API
    - all: show only groups that are not listed in the
      berlin.technical_groups config
    """
    LOG.info(f"request path: {c.request.path}")
    if c.request.path.endswith('/organization_list'):
        # `organization_list?all_fields=True` calls `group_show`.
        # because `group_show` for technical groups is not authorized
        # (see below), this would mean that all such calls to
        # `organization_list` would also fail as unauthorized. Making
        # a distinction based on the request path is a workaround.
        # Could also be solved in CKAN core (catching NotAuthorized in
        # logic.action.get._group_or_org_list).
        LOG.info("returning True")
        return { 'success': True }
    technical_groups = c.config.get("berlin.technical_groups", "")
    technical_groups = technical_groups.split(" ")
    group = Group.get(data_dict['id'])
    if group.name in technical_groups:
        return { 'success': False }
    else:
        return { 'success': True }

@plugins.toolkit.auth_disallow_anonymous_access
def task_status_show(context, data_dict):
    """Implementation of ckan.logic.auth.get.task_status_show

    - everyone: disallow
    """
    return {
        'success': False,
        'msg': 'You are not authorized to perform the task_status_show action.'
    }


@plugins.toolkit.auth_allow_anonymous_access
def user_show(context, data_dict):
    """Implementation of ckan.logic.auth.get.user_show

    - everyone: only allow to see self
    - sysadmin: can see everyone
    """

    # anonymous can call do user_show when coming from
    # /user/reset - otherwise resetting passwords is 
    # not possible
    if authz.auth_is_anon_user(context):
        if (c.request.path == "/user/reset"):
            return { 'success': True }
        else:
            return {
                'success': False ,
                'msg': 'Site access requires an authenticated user.'
            }

    model = context['model']

    _id = data_dict.get('id', None)
    provided_user = data_dict.get('user_obj', None)
    if _id:
        user_obj = model.User.get(_id)
    elif provided_user:
        user_obj = provided_user
    else:
        raise logic.NotFound

    requester = context.get('user', None)
    sysadmin = False
    if requester:
        sysadmin = authz.is_sysadmin(requester)
        requester_looking_at_own_account = requester == user_obj.name
        path = c.request.path
        if (sysadmin or requester_looking_at_own_account or path.startswith("/user/reset/")):
            return { 'success': True }
        else:
            return {
                'success': False ,
                'msg': 'You are only authorized to see your own user details.'
            }
    else:
        return {
            'success': False ,
            'msg': 'You are only authorized to see your own user details.'
        }


@plugins.toolkit.auth_disallow_anonymous_access
def vocabulary_show(context, data_dict):
    """Implementation of ckan.logic.auth.get.vocabulary_show

    - anonymous: disallow
    - all others: standard behaviour
    """
    return ckanget.vocabulary_show(context, data_dict)


@plugins.toolkit.auth_disallow_anonymous_access
def resource_view_list(context, data_dict):
    """Implementation of ckan.logic.auth.get.resource_view_list

    - anonymous: disallow
    - all others: standard behaviour
    """
    return ckanget.resource_view_list(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def resource_view_show(context, data_dict):
    """Implementation of ckan.logic.auth.get.resource_view_show

    - anonymous: disallow
    - all others: standard behaviour
    """
    return ckanget.resource_view_show(context, data_dict)

def status_show(context, data_dict):
    """Implementation of ckan.logic.auth.get.status_show

    - everyone: disallow
    """
    return {
        'success': False,
        'msg': 'You are not authorized to perform the status_show action.'
    }

@plugins.toolkit.auth_disallow_anonymous_access
def package_collaborator_list(context, data_dict):
    '''Checks if a user is allowed to list of collaborators from a dataset.
    '''
    return ckanget.package_collaborator_list(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def package_activity_list(context, data_dict):
    '''Checks if a user is allowed to see the list of activities from a dataset.
    '''
    return ckanget.package_activity_list(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def dataset_follower_count(context, data_dict):
    '''Checks if a user is allowed to see the number of followers of a dataset.'''
    return ckanget.dataset_follower_count(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def dataset_followee_count(context, data_dict):
    '''Checks if a user is allowed to see the number of datasets that are
      followed by a given user.'''
    return ckanget.dataset_followee_count(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def followee_count(context, data_dict):
    '''Checks if a user is allowed to see the number of objects that are
      followed by a given user.'''
    return ckanget.followee_count(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def group_followee_count(context, data_dict):
    '''Checks if a user is allowed to see the number of groups that are
      followed by a given user.'''
    return ckanget.group_followee_count(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def user_followee_count(context, data_dict):
    '''Checks if a user is allowed to see the number of users that are
      followed by a given user.'''
    return ckanget.user_followee_count(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def user_follower_count(context, data_dict):
    '''Checks if a user is allowed to see the number of followers of a user.'''
    return ckanget.user_follower_count(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def member_list(context, data_dict):
    '''Checks if a user is allowed to see the list of members a group has.'''
    requester = context.get('user', None)
    group_id = data_dict.get('id', None)
    if group_id and has_user_permission_for_group_or_org(group_id, requester, 'admin'):
        return ckanget.member_list(context, data_dict)
    else:
        return {
            'success': False,
            'msg': f"You are not authorized to perform the member_list action on the group '{group_id}'."
        }

@plugins.toolkit.auth_disallow_anonymous_access
def group_activity_list(context, data_dict):
    '''Checks if a user is allowed to see the list of activities from a group.'''
    requester = context.get('user', None)
    group_id = data_dict.get('id', None)
    if group_id and has_user_permission_for_group_or_org(group_id, requester, 'admin'):
        return ckanget.group_activity_list(context, data_dict)
    else:
        return {
            'success': False,
            'msg': f"You are not authorized to perform the group_activity_list action on the group '{group_id}'."
        }

@plugins.toolkit.auth_disallow_anonymous_access
def format_autocomplete(context, data_dict):
    '''Checks if a user is allowed to use the autocompletion endpoint for formats.'''
    return ckanget.format_autocomplete(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def package_autocomplete(context, data_dict):
    '''Checks if a user is allowed to use the autocompletion endpoint for packages.'''
    return ckanget.package_autocomplete(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def user_autocomplete(context, data_dict):
    '''Checks if a user is allowed to use the autocompletion endpoint for users.'''
    return ckanget.user_autocomplete(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def group_autocomplete(context, data_dict):
    '''Checks if a user is allowed to use the autocompletion endpoint for groups.'''
    return ckanget.group_autocomplete(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def organization_autocomplete(context, data_dict):
    '''Checks if a user is allowed to use the autocompletion endpoint for categories.'''
    return ckanget.organization_autocomplete(context, data_dict)

@plugins.toolkit.auth_disallow_anonymous_access
def organization_activity_list(context, data_dict):
    '''Checks if a user is allowed to see the activity list of an organization.'''
    requester = context.get('user', None)
    org_id = data_dict.get('id', None)
    if org_id and has_user_permission_for_group_or_org(org_id, requester, 'admin'):
        return ckanget.organization_activity_list(context, data_dict)
    else:
        return {
            'success': False,
            'msg': f"You are not authorized to perform the organization_activity_list action on the group '{org_id}'."
        }

@plugins.toolkit.auth_disallow_anonymous_access
def organization_follower_count(context, data_dict):
    '''Checks if a user is allowed to see the follower count of an organization.'''
    return ckanget.organization_follower_count(context, data_dict)
