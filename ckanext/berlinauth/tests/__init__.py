import pytest
import ckan.tests.factories as factories

TECHNORG = 'technorg'

@pytest.fixture
def sysadmin():
    '''Fixture to create a sysadmin user.'''
    return factories.Sysadmin(name='theadmin')

@pytest.fixture
def org_with_users(app, sysadmin):
    '''Fixture to create an organization with different kinds of users.'''
    users = {
        'admin': factories.User(name='org_admin'),
        'editor': factories.User(name='org_editor'),
    }
    org = factories.Organization(name='theorg')
    group = factories.Group(name='thegroup')

    for role, user in users.items():
        member = {
            'username': user['name'],
            'role': role,
            'id': org['name'],
        }
        app.post(
            url='/api/3/action/organization_member_create',
            json=member,
            extra_environ={'Authorization': sysadmin['apikey']},
        )

        member = {
            'username': user['name'],
            'role': role,
            'id': group['name'],
        }
        app.post(
            url='/api/3/action/group_member_create',
            json=member,
            extra_environ={'Authorization': sysadmin['apikey']},
        )

    return {
        'organization': org,
        'group': group,
        'users': users,
        'sysadmin': sysadmin
    }


