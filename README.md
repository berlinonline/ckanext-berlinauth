# ckanext-berlinauth

[![Tests](https://github.com/berlinonline/ckanext-berlinauth/workflows/Tests/badge.svg?branch=master)](https://github.com/berlinonline/ckanext-berlinauth/actions)
[![Code Coverage](http://codecov.io/github/berlinonline/ckanext-berlinauth/coverage.svg?branch=master)](http://codecov.io/github/berlinonline/ckanext-berlinauth?branch=master)

This plugin belongs to a set of plugins for the _Datenregister_ – the non-public [CKAN](https://ckan.org) instance that is part of Berlin's open data portal [daten.berlin.de](https://daten.berlin.de).
`ckanext-berlinauth` provides a custom authorization model.
Among other things, access for anonymous users is restricted, file upload is deactivated

The plugin implements the following CKAN interfaces:

- [IAuthFunctions](http://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IAuthFunctions)
- [IActions](http://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IActions)
- [IMiddleware](http://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IMiddleware)

## Requirements

This plugin has been tested with CKAN 2.9.8 (which requires Python 3).

## Register-mode

"Register-mode" is the implementation for the use case where we have CKAN as a separate "backend" system, only accessible to administrative staff who add and manage datasets.
In this scenario, CKAN is called the "Datenregister".

The general authorization model is as follows:

- Anonymous users have no access to the website (https://datenregister.berlin.de), except for the `/about` and `/datenschutzerklaerung`. All requests are redirected to the login page.
- Anonymous has access to a subset of the CKAN API (most GET-able functions) and the DCAT API.
- Logged-in users have restricted access to site and API.
  - no user list/show (except for self)
  - no vocabulary list/show
  - hide certain groups from `group_list`, `organization_list`
  - hide users except self from `group_show`, `organization_show`
  - ...
- File upload has been disabled.

## Monitoring, Liveness and Readiness Probes

The fact that the home page (`/`) is no longer available to anonymous users has implications for monitoring services such as liveness and readiness probes in Kubernetes.
If `ckanext-berlinauth` is installed and activated, such services should not point to the home page, but instead to a page that is available to anonymous users as well.
A good candidate is the info page at `/about`.

## Additional Configuration Options

- `berlin.technical_groups`:
A space-separated list of group/organizations that are considered 'technical'.
A technical organization is one which does not reflect a real-world organization, but has only been introduced to structure permissions.
Technical groups are hidden for non-sysadmin users.

```ini
berlin.technical_groups = simplesearch harvester-fis-broker
```

- `berlin.public_pages`:
By default, access to the Datenregister is restricted to logged-in users.
This setting contains a space-separated list of paths that should be visible to the public, i.e., to anonymous users.

```ini
berlin.public_pages = about datenschutzerklaerung
```

## Version Numbers for Plugins

The CKAN API's [status_show](https://docs.ckan.org/en/2.9/api/#ckan.logic.action.get.status_show) method includes a list of plugins as configured in the `ckan.plugins` setting.
`ckanext-berlinauth` includes an extended version of `status_show`  that also shows the version number of each plugin.
This assumes that the plugin module defines a `__version__` attribute that contains the version number.
If there is no `__version__` attribute, the version number will be `unknown`:

```json
{
  "help": "http://ckandev.bln/api/3/action/help_show?name=status_show",
  "success": true,
  "result": {
    "site_title": "Datenregister Dev",
    "site_description": "",
    "site_url": "http://ckandev.bln",
    "ckan_version": "2.9.8",
    "error_emails_to": null,
    "locale_default": "en",
    "extensions": {
      "stats": {
        "version": "unknown"
      },
      "berlintheme": {
        "version": "0.3.6"
      },
      "berlinauth": {
        "version": "0.2.6"
      }
    }
  }
}
```

## License

This material is copyright © [BerlinOnline Stadtportal GmbH & Co. KG](https://www.berlinonline.net/).

This extension is open and licensed under the GNU Affero General Public License (AGPL) v3.0.
Its full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html


