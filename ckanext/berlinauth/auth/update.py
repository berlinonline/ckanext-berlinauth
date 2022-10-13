# encoding: utf-8
"""Custom implementations of auth functions from ckan.logic.auth.create
"""


import logging
import ckan.logic.auth.update as ckanupdate

LOG = logging.getLogger(__name__)


def resource_update(context, data_dict):
    '''Implementation of ckan.logic.auth.update.resource_update
    
    - everyone (except sysadmins): disallow file uploads
    '''
    if 'upload' in data_dict:
        return {
            'success': False,
            'msg': "File upload is disabled."
        }
    else:
        return ckanupdate.resource_update(context, data_dict)
