"""A Custom middleware for preventing anonymous access to most of the site.

Based on https://github.com/datopian/ckanext-noanonaccess
"""

import logging
import re

import ckan.lib.base as base
import ckan.model as model
from ckan.plugins.toolkit import config, asbool

LOG = logging.getLogger(__name__)
USER_PROCESS_PAGES = [
    '/user/login',
    '/user/reset',
    '/user/logged_in'
]
ASSET_PATHS = [
    '/webassets',
    '/base',
    '/favicon.ico',
    '/_debug_toolbar'
]

def public_pages():
    public_paths = config.get("berlin.public_pages", "").split()
    return [f"/{path}" for path in public_paths]

class AuthMiddleware(object):
    def __init__(self, app, app_conf):
        self.app = app

    def __call__(self, environ, start_response):

        # List of extensions to be made accessible for dcat
        ext = config.get('ckanext.dcatde_berlin.formats', '').split()

        # List of catalog endpoints                                      
        catalog_endpoints = config.get('ckanext.dcatde_berlin.additional_endpoints', '').split() # dcatde_berlin can add additional endpoints
        catalog_endpoints.append('/catalog')


        # we putting only UI behind login so API paths should remain accessible
        if environ['PATH_INFO'].startswith('/api/'):
            return self.app(environ,start_response)
        elif 'repoze.who.identity' in environ or self._get_user_for_apikey(environ):
            # if logged in via browser cookies or API key, all pages accessible
            return self.app(environ,start_response)
        # dcat catalog endpoint is available to anonymous
        elif re.match(f"^{'|'.join(catalog_endpoints)}\.({'|'.join(ext)})$", environ['PATH_INFO']):
            return self.app(environ,start_response)
        # dcat dataset endpoint is available to anonymous
        elif re.match(f"^/dataset/.+?\.({'|'.join(ext)})$", environ['PATH_INFO']):
            return self.app(environ,start_response)
        elif re.match(f"^/dataset/.+?", environ['PATH_INFO']):
            if asbool(config.get('ckanext.dcat.enable_content_negotiation')):
                if 'dcat' in config['ckan.plugins'].split():
                    from ckanext.dcat.utils import CONTENT_TYPES
                    if environ.get('HTTP_ACCEPT') in CONTENT_TYPES.values():
                        return self.app(environ, start_response)
        # assets (css, js, images) should be accessible to all
        elif environ['PATH_INFO'].startswith(tuple(ASSET_PATHS)):
            return self.app(environ, start_response)
        # certain public pages should be available to all
        elif environ['PATH_INFO'].startswith(tuple(public_pages())):
            return self.app(environ, start_response)
        # otherwise only login/reset are accessible
        elif environ['PATH_INFO'].startswith(tuple(USER_PROCESS_PAGES)):
            return self.app(environ, start_response)

        url = environ.get('HTTP_X_FORWARDED_PROTO') \
            or environ.get('wsgi.url_scheme', 'http')
        url += '://'
        if environ.get('HTTP_HOST'):
            url += environ['HTTP_HOST']
        else:
            url += environ['SERVER_NAME']
        url += '/user/login'
        headers = [
            ('Location', url),
            ('Content-Length','0'),
            ('X-Robots-Tag', 'noindex, nofollow, noarchive')
            ]
        status = '307 Temporary Redirect'
        start_response(status, headers)
        return [b'']

    def _get_user_for_apikey(self, environ):
        # Adapted from https://github.com/ckan/ckan/blob/625b51cdb0f1697add59c7e3faf723a48c8e04fd/ckan/lib/base.py#L396
        apikey_header_name = config.get(base.APIKEY_HEADER_NAME_KEY,
                                        base.APIKEY_HEADER_NAME_DEFAULT)
        apikey = environ.get(apikey_header_name, '')
        if not apikey:
            # For misunderstanding old documentation (now fixed).
            apikey = environ.get('HTTP_AUTHORIZATION', '')
        if not apikey:
            apikey = environ.get('Authorization', '')
            # Forget HTTP Auth credentials (they have spaces).
            if ' ' in apikey:
                apikey = ''
        if not apikey:
            return None
        apikey = str(apikey)
        # check if API key is valid by comparing against keys of registered users
        query = model.Session.query(model.User)
        user = query.filter_by(apikey=apikey).first()
        return user
