# encoding: utf-8
"""CKAN Plugin which handles authorisation for the
Berlin Open Data Portal.
"""

import logging

import ckan.plugins as plugins
import ckanext.berlinauth.auth.get as auth_get
import ckanext.berlinauth.auth.create as auth_create
import ckanext.berlinauth.action.get as action_get

from ckanext.berlinauth.auth_middleware import AuthMiddleware

LOG = logging.getLogger(__name__)


class BerlinauthPlugin(plugins.SingletonPlugin):
    """Main plugin class.
    """
    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IMiddleware, inherit=True)

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
            'group_revision_list': auth_get.group_revision_list ,
            'member_roles_list': auth_get.member_roles_list ,
            'organization_revision_list': auth_get.organization_revision_list ,
            'package_revision_list': auth_get.package_revision_list ,
            'revision_list': auth_get.revision_list ,
            'user_list': auth_get.user_list ,
            'group_show': auth_get.group_show ,
            'resource_status_show': auth_get.resource_status_show ,
            'revision_show': auth_get.revision_show ,
            'task_status_show': auth_get.task_status_show ,
            'user_show': auth_get.user_show ,
            'vocabulary_show': auth_get.vocabulary_show ,
            'resource_view_list': auth_get.resource_view_list ,
            'resource_view_show': auth_get.resource_view_show ,
            'status_show': auth_get.status_show ,
            'package_collaborator_list': auth_get.package_collaborator_list ,
            'dataset_follower_count': auth_get.dataset_follower_count ,
            'package_activity_list': auth_get.package_activity_list ,
            'user_follower_count': auth_get.user_follower_count ,
            'user_followee_count': auth_get.user_followee_count ,
            'group_followee_count': auth_get.group_followee_count ,
            'dataset_followee_count': auth_get.dataset_followee_count ,
            'followee_count': auth_get.followee_count ,
            'group_activity_list': auth_get.group_activity_list ,
            'member_list': auth_get.member_list ,
            'vocabulary_list': auth_get.vocabulary_list ,
            'organization_list_for_user': auth_get.organization_list_for_user ,
            'format_autocomplete': auth_get.format_autocomplete ,
            'package_autocomplete': auth_get.package_autocomplete ,
            'user_autocomplete': auth_get.user_autocomplete ,
            'group_autocomplete': auth_get.group_autocomplete ,
            'organization_autocomplete': auth_get.organization_autocomplete ,
            'organization_activity_list': auth_get.organization_activity_list ,
            'organization_follower_count': auth_get.organization_follower_count ,

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

    # -------------------------------------------------------------------
    # Implementation IMiddleWare
    # -------------------------------------------------------------------

    def make_middleware(self, app, config):
        return AuthMiddleware(app, config)