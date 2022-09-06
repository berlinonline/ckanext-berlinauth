"""Tests for checking if our desired authorization model is indeed what
what is happening. We try to do a test for each available API function,
even if we did not change the standard behaviour for this function. This is
because future releases of CKAN might change the standard behaviour."""

import copy
import logging
import py
import pytest

import ckan.common as c
import ckan.logic as logic
import ckan.tests.factories as factories
import ckan.tests.helpers as test_helpers

from ckan import model

from ckanext.berlinauth.auth.get import _public_pages

PLUGIN_NAME = 'berlinauth'
LOG = logging.getLogger(__name__)

# The following are action functions that have no corresponding auth
# functions. Hopefully this will change in a future release of CKAN.
no_auth_function = {
    "am_following_dataset",
    "am_following_group",
    "am_following_user",
    "dataset_followee_count",
    "dataset_follower_count",
    "follow_dataset",
    "follow_group",
    "follow_user",
    "followee_count",
    "group_followee_count",
    "group_follower_count",
    "group_package_show",
    "member_list",
    "organization_follower_count",
    "recently_changed_packages_activity_list",
    "resource_search",
    "roles_show",
    "tag_search",
    "task_status_update_many",
    "term_translation_show",
    "term_translation_update_many",
    "unfollow_dataset",
    "unfollow_group",
    "unfollow_user",
    "user_followee_count",
    "user_follower_count",
}

parameterless_allowed = {
    "package_list",
    "current_package_list_with_resources",
    "group_list",
    "organization_list",
    "group_list_authz",
    "license_list",
    "tag_list",
    "package_search",
    "tag_search",
    "tag_autocomplete",
    "recently_changed_packages_activity_list",
}

parameterless_forbidden = {
    "get_site_user",
    "status_show",
    "vocabulary_list",
    "user_list",
    "organization_list_for_user",
    "dashboard_activity_list",
    "dashboard_new_activities_count",
    "member_roles_list",
    "config_option_list",
    "job_list",
}

userid_forbidden = {
    "am_following_user",
    "dataset_followee_count",
    "dataset_followee_list",
    "followee_count",
    "followee_list",
    "group_followee_count",
    "group_followee_list",
    "organization_followee_list",
    "package_collaborator_list_for_user",
    "user_activity_list",
    "user_followee_count",
    "user_followee_list",
    "user_follower_count",
    "user_follower_list",
    "user_show",
}

activityid_forbidden = {
    "activity_data_show",
    "activity_diff",
    "activity_show",
}

# @pytest.fixture
# def group():
#     '''Fixture to create a group'''
#     group = factories.Group()
#     return group

# @pytest.fixture
# def org():
#     '''Fixture to create an organization'''
#     org = factories.Organization()
#     return org

# @pytest.fixture
# def user(org, group):
#     '''Fixture to create a logged-in user.'''
#     user = model.User(name="vera_musterer", password=u"testtest")
#     model.Session.add(user)
#     model.Session.commit()

#     data = {
#         "id": org['id'],
#         "username": user.name,
#         "role": "editor"
#     }
#     test_helpers.call_action("organization_member_create", **data)

#     data = {
#         "id": group['id'],
#         "username": user.name,
#         "role": "editor"
#     }
#     test_helpers.call_action("group_member_create", **data)

#     return user


# @pytest.fixture
# def datasets(user, group, org):
#     '''Fixture to create some datasets.'''

#     dataset_dicts = [
#         {
#             "name": "zugriffsstatistik-daten-berlin-de",
#             "title": "Zugriffsstatistik daten.berlin.de",
#             "groups": [
#                 { "name": group['name'] }
#             ],
#             "owner_org": org['name'],
#             "tags": [
#                 { "name": "Open Data" },
#             ],
#             "resources": [
#                 {
#                     "name": "A CSV-File",
#                     "url": "https://path.to.some/data.csv",
#                     "format": "CSV"
#                 }
#             ]
#         }
#     ]

#     for dataset_dict in dataset_dicts:
#         test_helpers.call_action(
#             "package_create",
#             context={"user": user.id},
#             **dataset_dict
#         )

#     return dataset_dicts

# @pytest.fixture
# def activity(user, datasets):
#     '''Fixture to create an activity.'''
#     dataset = datasets[0]
#     activity = factories.Activity(
#         user_id=user.id,
#         object_id=dataset["name"],
#         activity_type="new package",
#         data={"package": copy.deepcopy(dataset), "actor": "Mrs Someone"},
#     )
#     return activity


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestSimpleGetable(object):
    '''Tests that check authorization for simple get-able API
    functions with no further parameters.'''

    @pytest.mark.parametrize("function", list(parameterless_allowed - no_auth_function))
    def test_anonymous_access_allowed_parameterless(self, app, function):
        '''Check that anonymous can access the specified parameterless
        API functions'''
        app.get(
            url=f"/api/3/action/{function}",
            status=200
        )

    @pytest.mark.parametrize("function", list(parameterless_forbidden - no_auth_function))
    def test_anonymous_access_forbidden_parameterless(self, app, function):
        '''Check that anonymous cannot access the specified parameterless
        API functions.'''
        app.get(
            url=f"/api/3/action/{function}",
            status=403
        )

@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestUserFunctions(object):
    '''Tests that check authorization for API functions on user objects.'''

    @pytest.mark.parametrize("function", list(userid_forbidden - no_auth_function))
    def test_anonymous_access_forbidden_userid(self, app, function):
        '''Check that anonymous can access the specified API functions
        with user id parameter.'''
        user = factories.User()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={user['id']}",
            status=403
        )

@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestActivityFunctions(object):
    '''Tests that check authorization for API functions on activity objects.'''

    extra_params = {
        "activity_diff": "&object_type=dataset",
        "activity_show": "&include_data=true"
    }

    @pytest.mark.parametrize("function", list(activityid_forbidden - no_auth_function))
    def test_anonymous_access_forbidden_activityid(self, app, function):
        '''Check that anonymous can access the specified API functions
        with an activity id parameter.'''
        user = factories.User()
        org = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=org['id'])
        activity = factories.Activity(
            user_id=user['id'],
            object_id=dataset['id'],
            activity_type="new package",
            data={"package": copy.deepcopy(dataset), "actor": "Mr Someone"},
        )
        extra_params = TestActivityFunctions.extra_params.get(function, "")
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={activity['id']}{extra_params}",
            status=403
       )



    # def test_user_show_forbidden_for_anonymous(self, app, user):
    #     '''Check that anonymous cannot show users.'''
    #     app.get(
    #         url="/api/3/action/user_show",
    #         query_string=f"id={user.name}",
    #         status=403
    #     )

    # def test_package_show_allowed_for_anonymous(self, app, datasets):
    #     '''Check that anonymous user can show packages.'''
    #     app.get(
    #         url="/api/3/action/package_show",
    #         query_string=f"id={datasets[0]['name']}",
    #         status=200
    #     )

    # def test_organization_show_allowed_for_anonymous(self, app, org):
    #     '''Check that anonymous user can show organizations.'''
    #     app.get(
    #         url="/api/3/action/organization_show",
    #         query_string=f"id={org['name']}",
    #         status=200
    #     )

    # def test_group_show_allowed_for_anonymous(self, app, group):
    #     '''Check that anonymous user can show groups.'''
    #     app.get(
    #         url="/api/3/action/group_show",
    #         query_string=f"id={group['name']}",
    #         status=200
    #     )

    # def test_tag_show_allowed_for_anonymous(self, app, datasets):
    #     '''Check that anonymous user can show tags.'''
    #     app.get(
    #         url="/api/3/action/tag_show",
    #         query_string=f"id={datasets[0]['tags'][0]['name']}",
    #         status=200
    #     )

    # def test_resource_show_allowed_for_anonymous(self, app, datasets):
    #     dataset = model.Package.get(datasets[0]['name'])
    #     resource_id = dataset.resources[0].id
    #     app.get(
    #         url="/api/3/action/resource_show",
    #         query_string=f"id={resource_id}",
    #         status=200
    #     )

# # should not work
# curl -X POST -d '{ "name": "testoburger" }' https://datenregister.stage.berlinonline.net/api/3/action/package_create | jq "."

# # should not work
# curl -X POST -d '{ "id": "webatlas-berlin-wms" }' https://datenregister.stage.berlinonline.net/api/3/action/package_delete | jq "."

