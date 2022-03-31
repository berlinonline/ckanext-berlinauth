# ckanext-berlinauth

[![Tests](https://github.com/berlinonline/ckanext-berlinauth/workflows/Tests/badge.svg?branch=master)](https://github.com/berlinonline/ckanext-berlinauth/actions)
[![Code Coverage](http://codecov.io/github/berlinonline/ckanext-berlinauth/coverage.svg?branch=master)](http://codecov.io/github/berlinonline/ckanext-berlinauth?branch=master)

This plugin belongs to a set of plugins for the _Datenregister_ – the non-public [CKAN](https://ckan.org) instance that is part of Berlin's open data portal [daten.berlin.de](https://daten.berlin.de).
`ckanext-berlinauth` provides a custom authorization model.

The plugin implements the following CKAN interfaces:

- [IAuthFunctions](http://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IAuthFunctions)
- [IActions](http://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IActions)

## Requirements

This plugin has been tested with CKAN 2.9.5 (which requires Python 3).

## Register-mode

"Register-mode" is the implementation for the use case where we have CKAN as a separate "backend" system, only accessible to administrative staff who add and manage datasets.
In this scenario, CKAN is called the "Datenregister".

Only `auth.get` and `auth.create` functions have been implemented, as the standard CKAN authorization model in combination with the `ckan.auth` config options is fine for update, patch and delete.

The general authorization model is as follows:

- no anonymous access to the website (https://datenregister.berlin.de)
- anonymous access to a subset of the API
- restricted access for logged-in users (administrative staff and select others)

  - no user list/show (except for self)
  - no vocabulary list/show
  - hide certain groups from `group_list`, `organization_list`
  - hide users except self from `group_show`, `organization_show`
  - ... 

## Additional Configuration Options

- `berlin.technical_groups`:
A space-separated list of group/organizations that are considered 'technical'.
A technical organization is one which does not reflect a real-world organization, but has only been introduced to structure permissions.
Technical groups are hidden for non-sysadmin users.

```ini
berlin.technical_groups = simplesearch harvester-fis-broker harvester-stromnetz-berlin
```

## License

This material is copyright © [BerlinOnline Stadtportal GmbH & Co. KG](https://www.berlinonline.net/).

This extension is open and licensed under the GNU Affero General Public License (AGPL) v3.0.
Its full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html


