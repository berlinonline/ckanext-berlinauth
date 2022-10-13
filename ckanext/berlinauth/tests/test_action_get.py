import json
import logging
import pytest

from flask import Flask

import ckan.common as c
import ckan.tests.factories as factories

from ckanext.berlinauth.tests import sysadmin, org_with_users

flask_app = Flask(__name__)
PLUGIN_NAME = 'berlinauth'
LOG = logging.getLogger(__name__)

@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestOrganizationList(object):
    '''Tests that check authorization for simple get-able API
    functions with no further parameters.'''

    def test_technical_group_excluded_for_anonymous(self, app):
        '''Test that organizations specified as 'technical' are not returned by 
           `organization_list` for anonymous users.'''
        technical_groups = c.config.get("berlin.technical_groups", "").split(" ")
        technical_name = technical_groups.pop()
        factories.Organization(name=technical_name)
        factories.Organization(name='regular')
        response = app.get(
            url=f"/api/3/action/organization_list",
            status=200
        )
        data = json.loads(response.body)
        result = data['result']
        assert technical_name not in result

        response = app.get(
            url=f"/api/3/action/organization_list",
            query_string=f"all_fields=True",
            status=200
        )
        data = json.loads(response.body)
        result = data['result']
        assert technical_name not in [org['name'] for org in result]

    # TODO: skip the following because of CKAN core's missing auth_user_obj bug:
    # not currently skipped because we temporarily allow organization_list_for_user for anonymous while this bug isn't fixed
    # @pytest.mark.skip(reason="doesn't work due to bug in CKAN core")
    def test_technical_group_excluded_for_regular(self, app):
        '''Test that organizations specified as 'technical' are not returned by 
           `organization_list` for regular logged-in users.'''
        technical_groups = c.config.get("berlin.technical_groups", "").split(" ")
        technical_name = technical_groups.pop()
        factories.Organization(name='foobar')
        with app.flask_app.app_context():
            LOG.info("testing... ")
            factories.Organization(name='regular')
            factories.Organization(name=technical_name)
            user = factories.User()
            extra_environ = {
                "Authorization": user['apikey']
            }
            # response = app.get(
            #     url=f"/api/3/action/organization_list",
            #     status=200,
            #     extra_environ=extra_environ
            # )
            # data = json.loads(response.body)
            # result = data['result']
            # assert technical_name not in result

            response = app.get(
                url=f"/api/3/action/organization_list",
                query_string=f"all_fields=True",
                status=200,
                extra_environ=extra_environ,
            )
            data = json.loads(response.body)
            result = data['result']
            assert technical_name not in [org['name'] for org in result]


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestOrganizationShow(object):
    '''Tests that check the behaviour of the API's `group_show` method.'''

    @pytest.mark.parametrize('group_type', [ 'organization', 'group' ])
    def test_sysadmin_can_see_all_members(self, app, org_with_users, group_type):
        '''Check that a sysadmin user can see all members of an org.'''
        
        sysadmin = org_with_users['sysadmin']
        response = app.get(
            url=f'/api/3/action/{group_type}_show',
            query_string=f"id={org_with_users[group_type]['name']}",
            extra_environ={'Authorization': sysadmin['apikey']},
            status=200,
        )

        data = json.loads(response.body)
        member_names = [ member['name'] for member in data['result']['users'] ]
        expected_names = [ user['name'] for user in org_with_users['users'].values() ]
        # we're checking for subset not equality, because organization_show will
        # also return the site_user
        assert set(expected_names).issubset(set(member_names))

    # TODO: skip the following because of CKAN core's missing auth_user_obj bug:
    # not currently skipped because we temporarily allow organization_list_for_user for anonymous while this bug isn't fixed
    # @pytest.mark.skip(reason="doesn't work due to bug in CKAN core")
    def test_org_admin_can_see_all_users(self, app, org_with_users):
        '''Check that an org's admin can see all of its members.'''

        group_admin = org_with_users['users']['admin']
        response = app.get(
            url=f'/api/3/action/organization_show',
            query_string=f"id={org_with_users['organization']['name']}",
            extra_environ={'Authorization': group_admin['apikey']},
            status=200,
        )

        data = json.loads(response.body)
        member_names = [ member['name'] for member in data['result']['users'] ]
        expected_names = [ user['name'] for user in org_with_users['users'].values() ]
        # we're checking for subset not equality, because organization_show will
        # also return the site_user
        assert set(expected_names).issubset(set(member_names))

    # TODO: skip the following because of CKAN core's missing auth_user_obj bug:
    # not currently skipped because we temporarily allow organization_list_for_user for anonymous while this bug isn't fixed
    # @pytest.mark.skip(reason="doesn't work due to bug in CKAN core")
    def test_regular_member_can_only_see_self(self, app, org_with_users):
        '''Check that a regular org member can only see themselves as a member.'''

        group_editor = org_with_users['users']['editor']
        group_admin = org_with_users['users']['admin']
        response = app.get(
            url=f'/api/3/action/organization_show',
            query_string=f"id={org_with_users['organization']['name']}",
            extra_environ={'Authorization': group_editor['apikey']},
            status=200,
        )

        data = json.loads(response.body)
        member_names = [ member['name'] for member in data['result']['users'] ]
        assert group_editor['name'] in member_names
        assert group_admin['name'] not in member_names

    @pytest.mark.parametrize('group_type', [ 'organization', 'group' ])
    def test_anonymous_cannot_see_members(self, app, org_with_users, group_type):
        '''Check that anonymous cannot see any org members.'''

        response = app.get(
            url=f'/api/3/action/{group_type}_show',
            query_string=f"id={org_with_users[group_type]['name']}",
            status=200,
        )

        data = json.loads(response.body)
        assert 'users' not in data
        # have non_admin call `group_show`
        # check that other_user is not in the returned list of org members
        # make same test with sysadmin user, check that all members are returned
