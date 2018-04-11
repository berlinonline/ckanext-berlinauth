# encoding: utf-8

import logging
import ckan.plugins as plugins
import ckan.logic.auth.get as ckanget
import ckan.common as c

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
  path = c.request.path
  log.debug(context.get('auth_user_obj'))
  if not path.startswith("/api"):
    return {'success': False, 'msg': 'Site access requires an authenticated user.'}
  else:
    return {'success': True}
  return ckanget.site_read(context, data_dict)

# xyz_list functions:

def group_revision_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.group_revision_list

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.group_revision_list(context, data_dict)

def member_roles_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.member_roles_list

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.member_roles_list(context, data_dict)


def organization_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.organization_list

  - anonymous: disallow
  - all others: standard behaviour
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

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.organization_revision_list(context, data_dict)


def package_revision_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.package_revision_list

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.package_revision_list(context, data_dict)


def revision_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.revision_list

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.revision_list(context, data_dict)

def user_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.user_list

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.user_list(context, data_dict)

def vocabulary_list(context, data_dict):
  """Implementation of ckan.logic.auth.get.vocabulary_list

  - anonymous: disallow
  - all others: standard behaviour
  """
  return ckanget.vocabulary_list(context, data_dict)

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


