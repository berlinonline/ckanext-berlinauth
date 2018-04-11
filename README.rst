.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/berlinonline/ckanext-berlinauth.svg?branch=master
    :target: https://travis-ci.org/berlinonline/ckanext-berlinauth

.. image:: https://coveralls.io/repos/berlinonline/ckanext-berlinauth/badge.svg
  :target: https://coveralls.io/r/berlinonline/ckanext-berlinauth

.. image:: https://pypip.in/download/ckanext-berlinauth/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-berlinauth/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-berlinauth/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-berlinauth/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-berlinauth/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-berlinauth/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-berlinauth/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-berlinauth/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-berlinauth/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-berlinauth/
    :alt: License

==================
ckanext-berlinauth
==================

Implements IAuthFunctions to achieve the authorization model for the CKAN
installation for "Offen Daten Berlin".

-------------
Register-mode
-------------

"Register-mode" is the implementation for the use case where we have CKAN
as a separate "backend" system, only accessible to administrative staff who 
add and manage datasets. In this scenario, CKAN is called the "Datenregister".

The general authorization model is as follows:

- no anonymous access to the website (https://datenregister.berlin.de)
- anonymous access to a subset of the API
- restricted access for logged-in users (administrative staff and select others)

  - no user list/show
  - no vocabulary list/show
  - ... 


------------
Requirements
------------

Has been tested with CKAN 2.7.3.


