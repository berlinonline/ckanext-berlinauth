# encoding: utf-8
"""Custom implementations of action functions from ckan.logic.action.get
"""

import logging
import ckan as ckan
import ckan.logic.action.get as ckanget
import ckan.common as c
from paste.deploy.converters import asbool

log = logging.getLogger(__name__)

@ckan.logic.side_effect_free
def organization_list(context, data_dict):
    """Implementation of ckan.logic.action.get.organization_list
    """
    org_list = ckanget.organization_list(context, data_dict)
    user = context.get('auth_user_obj', None)
    if not user or not user.sysadmin:
        technical_groups = c.config.get("berlin.technical_groups", "")
        technical_groups = technical_groups.split(" ")
        all_fields = asbool(data_dict.get('all_fields', None))
        if all_fields:
            org_list = list(filter(lambda x: x['name'] not in technical_groups, org_list))
        else:
            org_list = list(filter(lambda x: x not in technical_groups, org_list))
    return org_list


def _filter_group_show(context, group_dict):
    current_user = context.get('auth_user_obj', None)
    if not current_user:
        group_dict.pop('users', None)
    elif not current_user.sysadmin:
        users = group_dict.get('users', [])
        users = list(filter(lambda x: x['name'] == current_user.name, users))
        group_dict['users'] = users
    return group_dict


@ckan.logic.side_effect_free
def group_show(context, data_dict):
    """Implementation of ckan.logic.action.get.group_show
    """
    group_dict = ckanget.group_show(context, data_dict)
    group_dict = _filter_group_show(context, group_dict)
    return group_dict


@ckan.logic.side_effect_free
def organization_show(context, data_dict):
    """Implementation of ckan.logic.action.get.organization_show
    """
    group_dict = ckanget.organization_show(context, data_dict)
    group_dict = _filter_group_show(context, group_dict)
    return group_dict
