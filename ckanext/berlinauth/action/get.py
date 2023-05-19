# encoding: utf-8
"""Custom implementations of action functions from ckan.logic.action.get
"""

import importlib
import logging
import ckan as ckan
import ckan.logic.action.get as ckanget
import ckan.common as c
from ckan.plugins.toolkit import asbool

LOG = logging.getLogger(__name__)

@ckan.logic.side_effect_free
def organization_list(context, data_dict):
    """Implementation of ckan.logic.action.get.organization_list

    Hides groups/organizations included in berlin.technical_groups
    from everyone but sysadmins.
    """
    org_list = ckanget.organization_list(context, data_dict)
    user = context.get('auth_user_obj', None)
    if not user or not user.sysadmin:
        technical_groups = c.config.get("berlin.technical_groups", "")
        technical_groups = technical_groups.split(" ")
        all_fields = asbool(data_dict.get('all_fields', None))
        if all_fields:
            org_list = [x for x in org_list if x['name'] not in technical_groups]
        else:
            org_list = [x for x in org_list if x not in technical_groups]
    return org_list


def _filter_group_show(context, group_dict):
    """Filter the output of group_show / organization_show action
    functions to only show members which the requesting user is
    allowed to see:

    - logged_in: only self
    - group admin: all
    - sysadmin: all
    """
    from ckan.authz import has_user_permission_for_group_or_org
    current_user = context.get('auth_user_obj', None)
    if not current_user:
        group_dict.pop('users', None)
    elif not has_user_permission_for_group_or_org(group_dict['id'], current_user.name, 'admin'):
        users = group_dict.get('users', [])
        users = [x for x in users if x['name'] == current_user.name]
        group_dict['users'] = users
    return group_dict


@ckan.logic.side_effect_free
def group_show(context, data_dict):
    """Implementation of ckan.logic.action.get.group_show

    Only includes members in the 'users' attribute which the
    requesting user is allowed to see:

    - logged_in: only self
    - sysadmin: all
    """
    group_dict = ckanget.group_show(context, data_dict)
    group_dict = _filter_group_show(context, group_dict)
    return group_dict


@ckan.logic.side_effect_free
def organization_show(context, data_dict):
    """Implementation of ckan.logic.action.get.organization_show

    Only includes members in the 'users' attribute which the
    requesting user is allowed to see:

    - logged_in: only self
    - sysadmin: all
    """
    group_dict = ckanget.organization_show(context, data_dict)
    group_dict = _filter_group_show(context, group_dict)
    return group_dict


@ckan.logic.side_effect_free
def status_show(context, data_dict):
    '''Return a dictionary with information about the site's configuration.

    :rtype: dictionary

    '''

    def build_ext_dict(ext_name: str)->dict:
        ext_path = f"ckanext.{ext_name}"
        extension = importlib.import_module(ext_path)
        version = "unknown"
        if hasattr(extension, '__version__'):
            version = extension.__version__
        return { "name": ext_name, "version": version }


    LOG.info("custom status_show")
    status_dict = ckanget.status_show(context, data_dict)
    extensions = status_dict['extensions']
    LOG.info(f"extensions: {extensions}")
    extensions = [ build_ext_dict(ext_name) for ext_name in extensions ]
    LOG.info(f"extended extension: {extensions}")
    status_dict['extensions'] = extensions
    return status_dict
