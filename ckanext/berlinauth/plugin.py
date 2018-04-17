# encoding: utf-8

import ckan.plugins as plugins
import ckanext.berlinauth.auth.get as auth_get

class BerlinauthPlugin(plugins.SingletonPlugin):
  plugins.implements(plugins.IConfigurer, inherit=False)
  plugins.implements(plugins.IAuthFunctions)
  
  # -------------------------------------------------------------------
  # Implementation IConfigurer
  # -------------------------------------------------------------------

  def update_config(self, config):  

    # authentication stuff:
    # we can cover a lot of use cases already here
    config['ckan.auth.anon_create_dataset'] = False
    config['ckan.auth.create_unowned_dataset'] = False
    config['ckan.auth.create_dataset_if_not_in_organization'] = False
    config['ckan.auth.user_create_groups'] = False
    config['ckan.auth.user_create_organizations'] = False
    config['ckan.auth.user_delete_groups'] = False
    config['ckan.auth.user_delete_organizations'] = False
    config['ckan.auth.create_user_via_api'] = False
    config['ckan.auth.create_user_via_web'] = False
    config['ckan.auth.roles_that_cascade_to_sub_groups'] = 'admin'

    config['berlin.technical_groups'] = "simplesearch harvester-fis-broker harvester-stromnetz-berlin"

  # -------------------------------------------------------------------
  # Implementation IAuthFunctions
  # -------------------------------------------------------------------

  def get_auth_functions(self):
    return {
      # get
      'site_read': auth_get.site_read ,
      'group_revision_list': auth_get.group_revision_list ,
      'member_roles_list': auth_get.member_roles_list ,
      'organization_list': auth_get.organization_list ,
      'organization_list_for_user': auth_get.organization_list_for_user ,
      'organization_revision_list': auth_get.organization_revision_list ,
      'package_revision_list': auth_get.package_revision_list ,
      'revision_list': auth_get.revision_list ,
      'user_list': auth_get.user_list ,
      'vocabulary_list': auth_get.vocabulary_list ,
      'group_show': auth_get.group_show ,
      'resource_status_show': auth_get.resource_status_show ,
      'revision_show': auth_get.revision_show ,
      'task_status_show': auth_get.task_status_show ,
      'user_show': auth_get.user_show ,
      'vocabulary_show': auth_get.vocabulary_show ,
    }


# TODO:
# - _list and _show for logged_in users
# - blacklist/whitelist organizations


