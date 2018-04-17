# encoding: utf-8

import logging
import ckan.plugins as plugins
import ckan.logic.auth.get as ckanget
import ckan.common as c
import ckan.authz as authz
from ckan.model.group import Group

log = logging.getLogger(__name__)

@plugins.toolkit.auth_allow_anonymous_access
def site_read(context, data_dict=None):
  """Implementation of ckan.logic.auth.get.site_read

  anonymous:
  - allow api calls (path starts with "/api")
  - disallow everything else

  everyone else:
  - fall back to default behaviour of ckan.logic.auth.get.site_read
  """
  log.debug(" site_read")
  path = c.request.path
  if authz.auth_is_anon_user(context):
    log.debug(" user is anonymous")
    if not path.startswith("/api"):
      return {'success': False, 'msg': 'Site access requires an authenticated user.'}
    else:
      return {'success': True}
  else:
    log.debug(" user is logged_in")
    return ckanget.site_read(context, data_dict)

# xyz_list functions:
# egrep "def ([a-z_]+?_list(_[a-z_]+?)?)\(" ckan/logic/auth/get.py | sort | uniq

def group_revision_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.group_revision_list

  - everyone: disallow (revisions can only be seen by sysadmin)
  """
  return { 'success': False, 'msg': 'You are not authorized to perform the group_revision_list action.'}


def member_roles_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.member_roles_list

  - everyone: disallow
  """
  return { 'success': False, 'msg': 'You are not authorized to perform the member_roles_list action.'}


def organization_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.organization_list

  - anonymous: disallow
  - logged_in: show only those organizations for which group_show is true
    (implemented via CKAN Core)
  """
  return ckanget.organization_list(context, data_dict)


def organization_list_for_user(context, data_dict):
  """Implementation of ckan.logic.auth.get.organization_list_for_user

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.organization_list_for_user(context, data_dict)


def organization_revision_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.organization_revision_list

  - everyone: disallow (revisions can only be seen by sysadmin)
  """
  return { 'success': False, 'msg': 'You are not authorized to perform the organization_revision_list action.'}


def package_revision_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.package_revision_list

  - everyone: disallow
  """
  return { 'success': False, 'msg': 'You are not authorized to perform the package_revision_list action.'}


def revision_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.revision_list

  - everyone: disallow (revisions can only be seen by sysadmin)
  """
  return { 'success': False, 'msg': 'You are not authorized to perform the revision_list action.'}


def user_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.user_list

  - everyone: disallow
  """
  return { 'success': False, 'msg': 'You are not authorized to perform the user_list action.'}


def vocabulary_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.vocabulary_list

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.vocabulary_list(context, data_dict)


# xyz_show functions:
# egrep "def ([a-z_]+?_show(_[a-z_]+?)?)\(" ckan/logic/auth/get.py | sort | uniq

def group_show(context, data_dict):
  """Implementation of ckan.logic.auth.get.group_show

  - anonymous: disallow
  - logged_in: show only groups that are not listed in the
    berlin.technical_groups config
  """
  technical_groups = c.config.get("berlin.technical_groups", "")
  technical_groups = technical_groups.split(" ")
  group = Group.get(data_dict['id'])
  if (group.name in technical_groups):
    return { 'success': False }
  else:
    return { 'success': True }


def resource_status_show(context, data_dict):
  """Implementation of ckan.logic.auth.get.resource_status_show

    - everyone: disallow (method is deprecated)
  """
  return { 'success': False , 'msg': 'resource_status_show is deprecated'}


def revision_show(context, data_dict):
  """Implementation of ckan.logic.auth.get.revision_show

  - everyone: disallow (revisions can only be seen by sysadmin)
  """
  return { 'success': False, 'msg': 'You are not authorized to perform the revision_show action.'}


def task_status_show(context, data_dict):
  """Implementation of ckan.logic.auth.get.task_status_show

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.task_status_show(context, data_dict)


def user_show(context, data_dict):
  """Implementation of ckan.logic.auth.get.user_show

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.user_show(context, data_dict)


def vocabulary_show(context, data_dict):
  """Implementation of ckan.logic.auth.get.vocabulary_show

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.vocabulary_show(context, data_dict)


# Methods in ckan.logic.auth.get not implemented here
# (and why):

    # def _followee_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def config_option_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def current_package_list_with_resources(context, data_dict):
    # same as package_list

    # def dashboard_activity_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def dataset_followee_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def dataset_follower_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def followee_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def group_followee_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def group_follower_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def group_list(context, data_dict):
    # should be allowed for anonymous

    # def group_list_authz(context, data_dict):
    # same as group_list

    # def group_list_available(context, data_dict):
    # same as group_list

    # def job_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def license_list(context, data_dict):
    # should be allowed for anonymous

    # def organization_followee_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def organization_follower_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def package_list(context, data_dict):
    # should be allowed for anonymous

    # def package_relationships_list(context, data_dict):
    # standard behaviour allows if both is_authorized('package_show')
    # is true for both packages

    # def resource_view_list(context, data_dict):
    # should be allowed for anonymous

    # def tag_list(context, data_dict):
    # should be allowed for anonymous

    # def user_followee_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def user_follower_list(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def config_option_show(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def group_show_rest(context, data_dict):
    # same as group_show

    # def help_show(context, data_dict):
    # should be allowed for anonymous

    # def job_show(context, data_dict):
    # not allowed for anonymous in standard CKAN

    # def organization_show(context, data_dict):
    # same as group_show

    # def package_show(context, data_dict):
    # should be allowed for anonymous

    # def package_show_rest(context, data_dict):
    # should be allowed for anonymous

    # def resource_show(context, data_dict):
    # should be allowed for anonymous

    # def resource_view_show(context, data_dict):
    # should be allowed for anonymous

    # def tag_show(context, data_dict):
    # should be allowed for anonymous

    # def tag_show_rest(context, data_dict):
    # should be allowed for anonymous

    # def package_search(context, data_dict):
    # should be allowed for anonymous
