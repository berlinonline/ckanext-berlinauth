# encoding: utf-8
"""CKAN Plugin which handles authorisation for the
Berlin Open Data Portal.
"""

import ckan.plugins as plugins
import ckanext.berlinauth.auth.get as auth_get
import ckanext.berlinauth.auth.create as auth_create
import ckanext.berlinauth.action.get as action_get

class BerlinauthPlugin(plugins.SingletonPlugin):
    """Main plugin class.
    """
    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)

    # -------------------------------------------------------------------
    # Implementation IConfigurer
    # -------------------------------------------------------------------

    def update_config(self, config):
        """Implementation of IConfigurer.update_config()

        Config settings made in code by this plugin.
        """

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
        config['ckan.auth.allow_dataset_collaborators'] = True
        config['ckan.auth.roles_that_cascade_to_sub_groups'] = 'admin'

        config['berlin.technical_groups'] = \
            "simplesearch harvester-fis-broker harvester-stromnetz-berlin"

    # -------------------------------------------------------------------
    # Implementation IAuthFunctions
    # -------------------------------------------------------------------

    def get_auth_functions(self):
        """Implementation of IAuthFunctions.get_auth_functions()

        Authorization functions that are provided by this plugin.
        """
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
            'package_show': auth_get.package_show ,
            'group_list': auth_get.group_list ,
            'license_list': auth_get.license_list ,
            'package_list': auth_get.package_list ,
            'resource_view_list': auth_get.resource_view_list ,
            'tag_list': auth_get.tag_list ,
            'organization_show': auth_get.organization_show ,
            'resource_show': auth_get.resource_show ,
            'resource_view_show': auth_get.resource_view_show ,
            'tag_show': auth_get.tag_show ,
            'package_search': auth_get.package_search ,
            'status_show': auth_get.status_show ,
            'package_collaborator_list': auth_get.package_collaborator_list ,

            # create
            'rating_create': auth_create.rating_create ,
            'user_create': auth_create.user_create ,

            # update, path, delete: nothing to do, this
            # is all fine in standard CKAN / covered by
            # ckan.auth settings
        }

    # -------------------------------------------------------------------
    # Implementation IActions
    # -------------------------------------------------------------------

    def get_actions(self):
        """Implementation of IActions.get_actions()

        Actions functions that are provided by this plugin.
        """
        return {
            'group_show': action_get.group_show ,
            'organization_show': action_get.organization_show ,
            'organization_list': action_get.organization_list ,
        }
