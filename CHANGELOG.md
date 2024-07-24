# Changelog

## Development

- Allow authorization via tokens, in addition to browser cookies and api keys.

## [0.2.6](https://github.com/berlinonline/ckanext-berlinauth/releases/tag/0.2.6)

_(2023-05-22)_

- Modify the `status_show` API method to show the loaded extensions' version number, based on an `__version__`-attribute (or `unknown`).
- Define extension's version string in [VERSION](VERSION), make it available as `ckanext.berlinauth.__version__` and in [setup.py](setup.py).

## [0.2.5](https://github.com/berlinonline/ckanext-berlinauth/releases/tag/0.2.5)

_(2023-05-08)_

- Fix error when a registered non-admin user is looking at `/organization` and would see a technical group in the list of orgs (which they are not authorized to see).
- Fix error where password reset links were rejected.

## [0.2.4](https://github.com/berlinonline/ckanext-berlinauth/releases/tag/0.2.4)

_(2023-04-18)_

- We no longer configure `berlin.technical_groups` in the plugin initialization in, as this can mess with tests that also set this config option via `@pytest.mark.ckan_config()`. Instead, the option needs to be set in the ckan config file.
- Fix error in middleware (empty response body for redirects needs to be byte string).

## [0.2.3](https://github.com/berlinonline/ckanext-berlinauth/releases/tag/0.2.3)

_(2023-04-05)_

- Enable anonymous access to ckanext-dcat's RDF represesentations through content
  negotiation, not just through file suffixes.
- Simplify middleware code (fewer conditionals, better imports).
- Fix broken login workflow.

## [0.2.2](https://github.com/berlinonline/ckanext-berlinauth/releases/tag/0.2.2)

_(2023-01-23)_

- Add documentation about configuring monitoring services.
- Small adjustment to `MANIFEST.in`.

## [0.2.1](https://github.com/berlinonline/ckanext-berlinauth/releases/tag/0.2.1)

_(2022-10-25)_

- Change codecov upload in github CI, now using the recommended approach as defined in https://docs.codecov.com/docs#step-4-upload-coverage-reports-to-codecov.

## [0.2.0](https://github.com/berlinonline/ckanext-berlinauth/releases/tag/0.2.0)

_(2022-10-13)_

- Convert to Python 3.
- Add `berlin.public_pages` config setting to define pages that can be accessed by anonymous users (all other pages require login).
- Update README.
- This is the first version that requires Python 3 / CKAN >= 2.9.
- Implement the [IMiddleWare](https://docs.ckan.org/en/2.9/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IMiddleware) interface to handle handle access to specific pages and endpoints for anonymous users.
- Add a basic test for each GET-able API function, to ensure that anonymous access to the API is how we want it to be.
- Disable file upload by restricting the auth functions for `resource_create` and `resource_update`.
- Add Github CI.
- Reformat changelog, add dates and version links.

## [0.1.0](https://github.com/berlinonline/ckanext-berlinauth/releases/tag/0.1.0)

_(2020-07-28)_

- This is the last version to work with Python 2 / CKAN versions < 2.9.
