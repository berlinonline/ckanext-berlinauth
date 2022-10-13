"""Tests for checking if our desired authorization model is indeed what
is happening (for create methods)."""

import json
import pytest
import ckan.tests.factories as factories
from ckanext.berlinauth.tests import sysadmin, org_with_users

PLUGIN_NAME = 'berlinauth'

@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
def test_file_upload_disallowed_in_resource_update(app, org_with_users, tmp_path):
    '''Test that file upload is not allowed during resource updating.'''
    dataset = factories.Dataset(owner_org=org_with_users['organization']['id'])
    user = org_with_users['users']['admin']

    data = {
        'package_id': dataset['id'],
    }
    response = app.post(
            url='/api/3/action/resource_create',
            json=data,
            extra_environ={'Authorization': user['apikey']},
    )

    resource = json.loads(response.body)['result']

    # this should be allowed
    data = {
        'id': resource['id'],
        'description': 'Updated without upload',
    }
    app.post(
            url='/api/3/action/resource_update',
            json=data,
            extra_environ={'Authorization': user['apikey']},
            status=200
    )

    # this shouldn't be allowed
    data = {
        'id': resource['id'],
        'upload': 'data.csv',
        'description': 'Updated with upload',
    }
    app.post(
            url='/api/3/action/resource_update',
            json=data,
            extra_environ={'Authorization': user['apikey']},
            status=403
    )
