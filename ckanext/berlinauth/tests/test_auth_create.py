"""Tests for checking if our desired authorization model is indeed what
is happening (for create methods)."""

import pytest
import ckan.tests.factories as factories
from ckanext.berlinauth.tests import sysadmin, org_with_users

PLUGIN_NAME = 'berlinauth'

@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
def test_file_upload_disallowed_in_resource_create(app, org_with_users, tmp_path):
    '''Test that file upload is not allowed during resource creation.'''
    dataset = factories.Dataset(owner_org=org_with_users['organization']['id'])
    user = org_with_users['users']['admin']

    data = {
        'package_id': dataset['id'],
        'upload': 'data.csv',
    }
    app.post(
            url='/api/3/action/resource_create',
            json=data,
            extra_environ={'Authorization': user['apikey']},
            status=403
    )
