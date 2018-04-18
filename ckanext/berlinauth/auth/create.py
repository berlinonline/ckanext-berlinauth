# encoding: utf-8
"""Custom implementations of auth functions from ckan.logic.auth.create
"""


import logging
import ckan.logic.auth.create as ckancreate

log = logging.getLogger(__name__)


def rating_create(context, data_dict):
    """Implementation of ckan.logic.auth.create.rating_create

    - everyone: disallow

    This is dead code, as ckan.logic.action.create.rating_create never
    calls this. WTF?
    """
    return {'success': False, 'msg': 'create_rating is not supported.'}


def user_create(context, data_dict=None):
    """Implementation of ckan.logic.auth.create.user_create

    - anonymous: disallow
    - all others: standard behaviour

    Also handled by settings:
    - ckan.auth.create_user_via_api
    - ckan.auth.create_user_via_web
    """
    return ckancreate.user_create(context, data_dict)


# Functions in ckan.logic.auth.create not implemented here
# (and why):

    # def _group_or_org_member_create(context, data_dict):
    # covered by standard CKAN role model: only someone
    # with admin role can add members to a group or organization

    # def activity_create(context, data_dict):
    # only allowed for sysadmin in standard CKAN

    # def group_create(context, data_dict=None):
    # covered by ckan.auth.user_create_group setting

    # def group_create_rest(context, data_dict):
    # covered by ckan.auth.user_create_group setting

    # def group_member_create(context, data_dict):
    # covered by _group_or_org_member_create

    # def organization_create(context, data_dict=None):
    # covered by ckan.auth.user_create_organizations setting

    # def member_create(context, data_dict):
    # covered by standard CKAN role model: admins can 
    # add members to a group/organization, editors can
    # add/edit datasets, members cannot do anything except view

    # def organization_member_create(context, data_dict):
    # covered by _group_or_org_member_create

    # def package_create(context, data_dict=None):
    # covered by settings
    # - ckan.auth.anon_create_dataset
    # - ckan.auth.create_unowned_dataset
    # - ckan.auth.create_dataset_if_not_in_organization

    # def package_create_rest(context, data_dict):
    # same as package_create

    # def package_create_default_resource_views(context, data_dict):
    # same as package_update

    # def package_relationship_create(context, data_dict):
    # handled by package_update (return true if true for both packages)

    # def resource_create(context, data_dict):
    # handled by package_update

    # def resource_create_default_resource_views(context, data_dict):
    # same as resource_create

    # def resource_view_create(context, data_dict):
    # same as resource_create

    # def tag_create(context, data_dict):
    # only allowed for sysadmin in standard CKAN

    # def vocabulary_create(context, data_dict):
    # only allowed for sysadmin in standard CKAN

# Other functions from ckan.logic.auth.create

    # def file_upload(context, data_dict=None):
    # def user_invite(context, data_dict):
    # def _check_group_auth(context, data_dict):
