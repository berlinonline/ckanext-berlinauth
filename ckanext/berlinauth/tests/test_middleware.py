"""Tests for checking if our custom middleware is indeed doing what
we want it to do."""

import copy
import logging
import py
import pytest

import ckan.common as c
from ckan.lib import webassets_tools
from ckan.lib.helpers import url_for
from ckan.lib.mailer import create_reset_key
import ckan.logic as logic
import ckan.tests.factories as factories
import ckan.tests.helpers as test_helpers

from ckan import model

from ckanext.berlinauth.auth_middleware import USER_PROCESS_PAGES

PLUGIN_NAME = 'berlinauth'
LOG = logging.getLogger(__name__)
PUBLIC_PAGES = ['about']
DCAT_EXTENSIONS = ['ttl', 'rdf', 'jsonld']

@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME} berlintheme')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestAnonymousAccess(object):
    
    @classmethod
    def setup_class(cls):
        c.config['berlin.public_pages'] = " ".join(PUBLIC_PAGES)

    @pytest.mark.parametrize("page", PUBLIC_PAGES)
    def test_anonymous_public_pages_allowed(self, app, page):
        '''Test that anonymous can see pages that are configured as public
           pages.'''
        app.get(
            url=f"/{page}",
            status=200,
            follow_redirects=False,
        )

    @pytest.mark.parametrize("page", PUBLIC_PAGES)
    def test_anonymous_non_public_pages_forbidden(self, app, page):
        '''Test that anonymous cannot see pages that are not configured as public
           pages.'''
        c.config['berlin.public_pages'] = ""
        app.get(
            url=f"/{page}",
            status=307,
            follow_redirects=False,
        )

    def test_api_allowed(self, app):
        '''Test that the API is reachable for anonymous in general. For more detailed
           tests for different API methods see test_auth_get.py.'''
        app.get(
            url="/api/3/action/package_list",
            status=200,
            follow_redirects=False,
        )

    @pytest.mark.parametrize("page", USER_PROCESS_PAGES)
    def test_user_process_pages_allowed(self, app, page):
        '''Test that anonymous can see pages that are involved in the user login/
           reset process.'''
        app.get(
            url=page,
            status=200,
            follow_redirects=False,
        )
    
    @pytest.mark.parametrize("page", ["group", "dataset", "user"])
    def test_disallowed_pages_sanity_check(self, app, page):
        '''Test that general access to the site is not allowed for anonymous by
           trying to open a handful of pages. Specififally, check that there
           is a redirect to /user/login.'''
        response = app.get(
            url=page,
            status=307,
            follow_redirects=False,
        )
        redirect_location = response.headers['Location']
        assert redirect_location.endswith('/user/login') 
        app.get(
            url=redirect_location,
            status=200
        )

    def test_reset_link_accessible_for_anonymous(self, app):
        '''Test that an anonymous user can access a password reset link.'''
        user = factories.User()
        user_obj = model.User.get(user['id'])
        create_reset_key(user_obj)
        reset_link = url_for(
            controller="user",
            action="perform_reset",
            id=user_obj.id,
            key=user_obj.reset_key,
        )
        app.get(
            url=reset_link,
            follow_redirects=False,
            status=200
        )
    
    def test_reset_link_accessible_for_logged_in(self, app):
        '''Test that an anonymous user can access a password reset link.'''
        user = factories.User()
        user_obj = model.User.get(user['id'])
        create_reset_key(user_obj)
        reset_link = url_for(
            controller="user",
            action="perform_reset",
            id=user_obj.id,
            key=user_obj.reset_key,
        )
        app.get(
            url=reset_link,
            follow_redirects=False,
            status=200,
            extra_environ={
                "Authorization": user['apikey']
            }
        )
    
    def test_reset_link_wrong_user_404(self, app):
        '''Test that an anonymous user gets a 404 when accessing a password reset link
           for a non-existant user.'''
        user = factories.User()
        user_obj = model.User.get(user['id'])
        create_reset_key(user_obj)
        reset_link = url_for(
            controller="user",
            action="perform_reset",
            id=user_obj.id[:-1],
            key=user_obj.reset_key,
        )
        app.get(
            url=reset_link,
            follow_redirects=False,
            status=404
        )


@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestAnonymousAssetAccess(object):

    @pytest.mark.parametrize('asset', 
        [bundle.urls().pop() for bundle in list(webassets_tools.env)],
    )
    def test_assets_allowed(self, app, asset):
        '''Test that local assets are available to anonymous.'''
        app.get(
            url=asset,
            status=200
        )
    

@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME} dcat')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
@pytest.mark.ckan_config('ckanext.dcatde_berlin.formats', ' '.join(DCAT_EXTENSIONS))
class TestAnonymousDCATAccess(object):

    def test_registered_catalog_allowed(self, app):
        '''Test that anonymous can access the DCAT extension's catalog endpoint with
           a registered file extension.'''
        app.get(
            url='/catalog.ttl',
            status=200,
            follow_redirects=False,
        )

    def test_unregistered_catalog_forbidden(self, app):
        '''Test that anonymous cannot access the DCAT extension's catalog endpoint with
           an unregistered file extension.'''
        app.get(
            url='/catalog.xml',
            status=307,
            follow_redirects=False,
        )

    def test_dataset_allowed(self, app):
        '''Test that anonymous can access the DCAT extension's dataset endpoint.'''
        user = factories.User()
        org = factories.Organization(user=user)
        dataset = factories.Dataset(owner_org=org['id'])
        app.get(
            url=f"/dataset/{dataset['id']}.ttl",
            status=200,
            follow_redirects=False,
        )

@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME} berlintheme')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestLoggedInAccess(object):

    c.config['berlin.public_pages'] = "about"

    def test_non_public_pages_allowed(self, app):
        '''Test that logged in users can see pages that have not
           been marked as public pages.'''
        user = factories.User()
        extra_environ = {
            "Authorization": user['apikey']
        }
        app.get(
            url=f"/datenschutzerklaerung",
            status=200,
            follow_redirects=False,
            extra_environ=extra_environ,
        )

@pytest.mark.ckan_config('ckan.plugins', f'{PLUGIN_NAME}')
@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_plugins')
class TestEdgeCases(object):

    def test_no_http_host(self, app):
        '''Test the edge case where the request has no HTTP_HOST set.'''
        extra_environ = {
            "HTTP_HOST": "",
        }
        app.get(
            url="/dataset",
            extra_environ=extra_environ,
            follow_redirects=False,
            status=307
        )

    def test_spaces_in_apikey(self, app):
        '''Test the edge case where there a spaces in a request's api key.'''
        extra_environ = {
            "Authorization": 'one two'
        }
        app.get(
            url=f"/dataset",
            status=307,
            follow_redirects=False,
            extra_environ=extra_environ,
        )
