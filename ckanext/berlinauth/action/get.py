# encoding: utf-8

import logging
import ckan.plugins as plugins
import ckan.logic.action.get as ckanget
import ckan.common as c
import ckan.authz as authz
from ckan.model.group import Group
from paste.deploy.converters import asbool

log = logging.getLogger(__name__)

def organization_list(context, data_dict):
    organization_list = ckanget.organization_list(context, data_dict)
    user = context.get('auth_user_obj', None)
    if not user or not user.sysadmin:
        technical_groups = c.config.get("berlin.technical_groups", "")
        technical_groups = technical_groups.split(" ")
        all_fields = asbool(data_dict.get('all_fields', None))
        if all_fields:
            organization_list = list(filter(lambda x: x['name'] not in technical_groups, organization_list))
        else:
            organization_list = list(filter(lambda x: x not in technical_groups, organization_list))
    return organization_list