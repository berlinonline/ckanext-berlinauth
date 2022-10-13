"""Tests for checking if our desired authorization model is indeed what
is happening. We try to do a test for each available API function,
even if we did not change the standard behaviour for this function. This is
because future releases of CKAN might change the standard behaviour."""

import copy
import logging
import pytest

import ckan.common as c
import ckan.tests.factories as factories

from ckan import model

from ckanext.berlinauth.tests import sysadmin, org_with_users

PLUGIN_NAME = 'berlinauth'
LOG = logging.getLogger(__name__)

# The following are action functions that have no corresponding auth
# functions (yet).
no_auth_function = {
    "follow_dataset",
    "follow_group",
    "follow_user",
    "roles_show",
    "task_status_update_many",
    "term_translation_update_many",
    "unfollow_dataset",
    "unfollow_group",
    "unfollow_user",
}

auth_settings = {
    "anonymous": {
        "parameterless_allowed": {
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
            # TODO: temporarily allowed because of CKAN core's missing auth_user_obj bug
            "organization_list_for_user",
        },
        "parameterless_forbidden": {
            "get_site_user",
            "status_show",
            "vocabulary_list",
            "user_list",
            "dashboard_activity_list",
            "dashboard_new_activities_count",
            "member_roles_list",
            "config_option_list",
            "job_list",
        },
        "user_id_forbidden": {
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
        },
        "activity_id_forbidden": {
            "activity_data_show",
            "activity_diff",
            "activity_show",
        },
        "dataset_id_allowed": {
            "package_relationships_list",
            "package_show",
        },
        "dataset_id_forbidden": {
            "am_following_dataset",
            "package_activity_list",
            "package_collaborator_list",
            "dataset_follower_count",
            "dataset_follower_list",
        },
        "group_id_allowed": {
            "group_follower_count" ,
            "group_package_show",
            "group_show",
        },
        "group_id_forbidden": {
            "am_following_group" ,
            "group_activity_list" ,
            "group_follower_list" ,
            "member_list" ,
        },
        "organization_id_allowed": {
            "organization_show" ,
        },
        "organization_id_forbidden": {
            "organization_activity_list" ,
            "organization_follower_count" ,
            "organization_follower_list" ,
        },
        "autocomplete_forbidden": {
            "format_autocomplete" ,
            "package_autocomplete" ,
            "user_autocomplete" ,
            "group_autocomplete" ,
            "organization_autocomplete" ,
        },
        "resource_id_allowed": {
            'resource_show' ,
        },
        "resource_id_forbidden": {
            'resource_view_list' ,
        },
        "resource_view_id_forbidden": {
            'resource_view_show' ,
        },
        "tag_id_allowed": {
            'tag_show' ,
        },
        "vocabulary_id_forbidden": {
            'vocabulary_show'
        }
    },
    "logged_in": {
        "parameterless_allowed": {
            "package_list",
            "group_list",
            "organization_list",
            "group_list_authz",
            "license_list",
            "tag_list",
            "tag_search",
            "tag_autocomplete",
            "recently_changed_packages_activity_list",
            "vocabulary_list",
            "organization_list_for_user",
            "dashboard_activity_list",
            "dashboard_new_activities_count",
            # TODO: the following fail because of CKAN core's missing auth_user_obj bug:
            # not currently skipped because we temporarily allow organization_list_for_user for anonymous while this bug isn't fixed
            "current_package_list_with_resources",
            "package_search",
        },
        "parameterless_forbidden": {
            "get_site_user",
            "status_show",
            "user_list",
            "member_roles_list",
            "config_option_list",
            "job_list",
        },
        "user_id_allowed": {
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
            "user_show",
        },
        "user_id_forbidden": {
            "user_follower_list",
        },
        "activity_id_allowed": {
            "activity_data_show",
            "activity_diff",
            "activity_show",
        },
        "dataset_id_allowed": {
            "package_relationships_list",
            "package_show",
            "am_following_dataset",
            "package_activity_list",
            "package_collaborator_list",
            "dataset_follower_count",
        },
        "dataset_id_forbidden": {
            "dataset_follower_list",
        },
        "group_id_allowed": {
            "am_following_group" ,
            "group_follower_count" ,
            "group_package_show",
            "group_show",
        },
        "group_id_forbidden": {
            "group_activity_list" ,
            "group_follower_list" ,
            "member_list" ,
        },
        "organization_id_allowed": {
            "organization_show" ,
            "organization_follower_count" ,
        },
        "organization_id_forbidden": {
            "organization_activity_list" ,
            "organization_follower_list" ,
        },
        "autocomplete_allowed": {
            "format_autocomplete" ,
            "package_autocomplete" ,
            "group_autocomplete" ,
            "organization_autocomplete" ,
        },
        "autocomplete_forbidden": {
            "user_autocomplete" ,
        },
        "resource_id_allowed": {
            'resource_show' ,
            'resource_view_list' ,
        },
        "resource_view_id_allowed": {
            'resource_view_show' ,
        },
        "tag_id_allowed": {
            'tag_show' ,
        },
        "vocabulary_id_forbidden": {
            'vocabulary_show'
        }
    }
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

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['parameterless_allowed'] - no_auth_function))
    def test_anonymous_access_allowed_parameterless(self, app, function):
        '''Check that anonymous can access the specified parameterless
        API functions.'''
        app.get(
            url=f"/api/3/action/{function}",
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['parameterless_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_parameterless(self, app, function):
        '''Check that anonymous cannot access the specified parameterless
        API functions.'''
        app.get(
            url=f"/api/3/action/{function}",
            status=403
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['parameterless_allowed'] - no_auth_function))
    def test_logged_in_access_allowed_parameterless(self, app, function):
        '''Check that logged-in users can access the specified parameterless
        API functions.'''
        user = factories.User()
        app.get(
            url=f"/api/3/action/{function}",
            extra_environ={'Authorization': user['apikey']},
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['parameterless_forbidden'] - no_auth_function))
    def test_logged_in_access_forbidden_parameterless(self, app, function):
        '''Check that logged-in users cannot access the specified parameterless
        API functions.'''
        user = factories.User()
        app.get(
            url=f"/api/3/action/{function}",
            extra_environ={'Authorization': user['apikey']},
            status=403
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestUserFunctions(object):
    '''Tests that check authorization for API functions on user objects.'''

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['user_id_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_userid(self, app, function):
        '''Check that anonymous can access the specified API functions
        with user id parameter.'''
        user = factories.User()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={user['id']}",
            status=403
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['user_id_allowed'] - no_auth_function))
    def test_logged_in_access_allowed_userid(self, app, function):
        '''Check that logged-in users can access the specified API functions
        with user id parameter.'''
        user = factories.User()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={user['id']}",
            extra_environ={'Authorization': user['apikey']},
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['user_id_forbidden'] - no_auth_function))
    def test_logged_in_access_forbidden_userid(self, app, function):
        '''Check that logged-in users cannot access the specified API functions
        with user id parameter.'''
        user = factories.User()
        app.get(
            url=f"/api/3/action/{function}",
            extra_environ={'Authorization': user['apikey']},
            status=403
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestActivityFunctions(object):
    '''Tests that checks authorization for API functions on activity objects.'''

    extra_params = {
        "activity_diff": "&object_type=package",
        "activity_show": "&include_data=true"
    }

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['activity_id_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_activityid(self, app, function):
        '''Check that anonymous cannot access the specified API functions
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

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['activity_id_allowed'] - no_auth_function))
    def test_logged_in_access_allowed_activityid(self, app, function):
        '''Check that a logged in user can access the specified API functions
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
            extra_environ={'Authorization': user['apikey']},
            status=200
       )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestDatasetFunctions(object):
    '''Tests that check authorization for API functions on dataset objects.'''

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['dataset_id_allowed'] - no_auth_function))
    def test_anonymous_access_allowed_datasetid(self, app, function):
        user = factories.User()
        org = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=org['id'])
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={dataset['id']}",
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['dataset_id_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_datasetid(self, app, function):
        user = factories.User()
        org = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=org['id'])
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={dataset['id']}",
            status=403
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['dataset_id_allowed'] - no_auth_function))
    def test_logged_in_access_allowed_datasetid(self, app, function):
        user = factories.User()
        org = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=org['id'])
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={dataset['id']}",
            extra_environ={'Authorization': user['apikey']},
            status=200
       )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['dataset_id_forbidden'] - no_auth_function))
    def test_logged_in_access_forbidden_datasetid(self, app, function):
        user = factories.User()
        org = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=org['id'])
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={dataset['id']}",
            extra_environ={'Authorization': user['apikey']},
            status=403
       )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestGroupFunctions(object):
    '''Tests that check authorization for API functions on group objects.'''

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['group_id_allowed'] - no_auth_function))
    def test_anonymous_access_allowed_group_id(self, app, function):
        group = factories.Group()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={group['id']}",
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['group_id_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_group_id(self, app, function):
        group = factories.Group()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={group['id']}",
            status=403
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['group_id_allowed'] - no_auth_function))
    def test_logged_in_access_allowed_group_id(self, app, function):
        user = factories.User()
        group = factories.Group()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={group['id']}",
            extra_environ={'Authorization': user['apikey']},
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['group_id_forbidden'] - no_auth_function))
    def test_logged_in_access_forbidden_group_id(self, app, function):
        user = factories.User()
        group = factories.Group()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={group['id']}",
            extra_environ={'Authorization': user['apikey']},
            status=403
        )

    def test_only_sysadmin_see_technical_orgs(self, app):
        '''Check that only sysadmins can see groups (or orgs) that have been defined
           as 'technical'.'''
        technical_groups = c.config.get("berlin.technical_groups", "").split(" ")
        technical_name = technical_groups.pop()
        org = factories.Organization(name=technical_name)
        app.get(
            url='/api/3/action/organization_show',
            query_string=f'id={technical_name}',
            status=403
        )

        user = factories.User()
        app.get(
            url='/api/3/action/organization_show',
            query_string=f'id={technical_name}',
            extra_environ={'Authorization': user['apikey']},
            status=403
        )
        
        sysadmin = factories.Sysadmin(name='theadmin')
        app.get(
            url='/api/3/action/organization_show',
            query_string=f'id={technical_name}',
            extra_environ={'Authorization': sysadmin['apikey']},
            status=200
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestOrganizationFunctions(object):
    '''Tests that check authorization for API functions on organization objects.'''

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['organization_id_allowed'] - no_auth_function))
    def test_anonymous_access_allowed_organization_id(self, app, function):
        org = factories.Organization()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={org['id']}",
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['organization_id_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_organization_id(self, app, function):
        org = factories.Organization()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={org['id']}",
            status=403
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['organization_id_allowed'] - no_auth_function))
    def test_logged_in_access_allowed_organization_id(self, app, function):
        user = factories.User()
        org = factories.Organization()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={org['id']}",
            extra_environ={'Authorization': user['apikey']},
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['organization_id_forbidden'] - no_auth_function))
    def test_logged_in_access_forbidden_organization_id(self, app, function):
        user = factories.User()
        org = factories.Organization()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={org['id']}",
            extra_environ={'Authorization': user['apikey']},
            status=403
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestAutocompleteFunctions(object):
    '''Tests that check authorization for autocomplete API functions.'''

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['autocomplete_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_autocomplete(self, app, function):
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"q=foo",
            status=403
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['autocomplete_allowed'] - no_auth_function))
    def test_logged_in_access_allowed_autocomplete(self, app, function):
        user = factories.User()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"q=foo",
            extra_environ={'Authorization': user['apikey']},
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['autocomplete_forbidden'] - no_auth_function))
    def test_logged_in_access_forbidden_autocomplete(self, app, function):
        user = factories.User()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"q=foo",
            extra_environ={'Authorization': user['apikey']},
            status=403
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestResourceFunctions(object):
    '''Tests that check authorization for API functions on resource objects.'''

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['resource_id_allowed'] - no_auth_function))
    def test_anonymous_access_allowed_resource_id(self, app, function):
        user = factories.User()
        organization = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=organization["id"])
        resource = factories.Resource(package_id=dataset["id"])
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={resource['id']}",
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['resource_id_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_resource_id(self, app, function):
        user = factories.User()
        organization = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=organization["id"])
        resource = factories.Resource(package_id=dataset["id"])
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={resource['id']}",
            status=403
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['resource_id_allowed'] - no_auth_function))
    def test_logged_in_access_allowed_resource_id(self, app, function):
        user = factories.User()
        organization = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=organization["id"])
        resource = factories.Resource(package_id=dataset["id"])
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={resource['id']}",
            extra_environ={'Authorization': user['apikey']},
            status=200
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME} image_view')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestResourceViewFunctions(object):
    '''Tests that check authorization for API functions on resource view objects.'''

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['resource_view_id_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_resource_view_id(self, app, function):
        user = factories.User()
        organization = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=organization["id"])
        resource = factories.Resource(package_id=dataset["id"])
        resource_view = factories.ResourceView(resource_id=resource["id"])
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={resource_view['id']}",
            status=403
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['resource_view_id_allowed'] - no_auth_function))
    def test_logged_in_access_forbidden_resource_view_id(self, app, function):
        user = factories.User()
        organization = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=organization["id"])
        resource = factories.Resource(package_id=dataset["id"])
        resource_view = factories.ResourceView(resource_id=resource["id"])
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={resource_view['id']}",
            extra_environ={'Authorization': user['apikey']},
            status=200
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestTagFunctions(object):
    '''Tests that check authorization for API functions on tag objects.'''

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['tag_id_allowed'] - no_auth_function))
    def test_anonymous_access_allowed_tag_id(self, app, function):
        tag = {"name": "my-tag"}
        user = factories.User()
        organization = factories.Organization(user=user)
        factories.Dataset(
            owner_org=organization["id"],
            name="dataset-one",
            title="Dataset One",
            tags=[tag]
        )
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={tag['name']}",
            status=200
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['tag_id_allowed'] - no_auth_function))
    def test_logged_in_access_allowed_tag_id(self, app, function):
        tag = {"name": "my-tag"}
        user = factories.User()
        organization = factories.Organization(user=user)
        factories.Dataset(
            owner_org=organization["id"],
            name="dataset-one",
            title="Dataset One",
            tags=[tag]
        )
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={tag['name']}",
            extra_environ={'Authorization': user['apikey']},
            status=200
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestVocabularyFunctions(object):
    '''Tests that check authorization for API functions on vocabulary objects.'''

    @pytest.mark.parametrize("function", list(auth_settings['anonymous']['vocabulary_id_forbidden'] - no_auth_function))
    def test_anonymous_access_forbidden_vocabulary_id(self, app, function):
        vocab = model.Vocabulary(u'genre')
        model.Session.add(vocab)
        sonata_tag = model.Tag(name=u'sonata', vocabulary_id=vocab.id)
        model.Session.add(sonata_tag)
        model.Session.commit()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={vocab.id}",
            status=403
        )

    @pytest.mark.parametrize("function", list(auth_settings['logged_in']['vocabulary_id_forbidden'] - no_auth_function))
    def test_logged_in_access_allowed_vocabulary_id(self, app, function):
        user = factories.User()
        vocab = model.Vocabulary(u'genre')
        model.Session.add(vocab)
        sonata_tag = model.Tag(name=u'sonata', vocabulary_id=vocab.id)
        model.Session.add(sonata_tag)
        model.Session.commit()
        app.get(
            url=f"/api/3/action/{function}",
            query_string=f"id={vocab.id}",
            extra_environ={'Authorization': user['apikey']},
            status=200
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestVariousFunctions(object):
    '''Tests that check authorization for various API functions that don't belong to a group.'''

    def test_anonymous_access_allowed_resource_search(self, app):
        '''Check that anonymous can call resource_search.'''
        user = factories.User()
        organization = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=organization["id"])
        factories.Resource(package_id=dataset["id"], format="XLS")
        app.get(
            url="/api/3/action/resource_search",
            query_string="query=format:XLS",
            status=200,
        )

    def test_anonymous_access_allowed_help_show(self, app):
        '''Check that anonymous can call help_show.'''
        app.get(
            url="/api/3/action/help_show",
            query_string="name=package_list",
            status=200,
        )

    def test_anonymous_access_forbidden_config_option_show(self, app):
        '''Check that anonymous cannot call config_option_show.'''
        app.get(
            url="/api/3/action/config_option_show",
            query_string="key=ckan.site_title",
            status=403,
        )

    def test_anonymous_access_allowed_term_translation_show(self, app):
        '''Check that anonymous can call term_translation_show.'''
        app.get(
            url="/api/3/action/term_translation_show",
            query_string="terms=fuel",
            status=200
        )

    def test_anonymous_access_forbidden_api_token_list(self, app):
        '''Check that anonymous cannot call api_token_list.'''
        app.get(
            url="/api/3/action/api_token_list",
            query_string="user=foo",
            status=403,
        )

    def test_anonymous_access_forbidden_task_status_show(self, app):
        '''Check that anonymous cannot call task_status_show.'''
        app.get(
            url="/api/3/action/task_status_show",
            query_string="id=foo",
            status=403,
        )

    def test_anonymous_access_forbidden_job_show(self, app):
        '''Check that anonymous cannot call job_show.'''
        app.get(
            url="/api/3/action/job_show",
            query_string="id=foo",
            status=403,
        )


