# encoding: utf-8

import ckan.plugins as plugins
class BerlinauthPlugin(plugins.SingletonPlugin):
  plugins.implements(plugins.IConfigurer, inherit=False)
  plugins.implements(plugins.IAuthFunctions)
  
  # -------------------------------------------------------------------
  # Implementation IConfigurer
  # -------------------------------------------------------------------

  def update_config(self, config):  

    # authentication stuff:
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

  # -------------------------------------------------------------------
  # Implementation IAuth
  # -------------------------------------------------------------------

  def get_auth_functions(self):
    return {
    }

