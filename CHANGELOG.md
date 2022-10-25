# Changelog

## Development

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
