|PyPI Version| |Python Version| |Django Version| |GitHub Actions| |Code Style| |License|

Welcome to Simple JWT MongoEngine's documentation!
==================================================

.. |PyPI Version| image:: https://img.shields.io/pypi/v/djangorestframework-simplejwt-mongoengine
   :target: https://github.com/ngocngoan/djangorestframework-simplejwt-mongoengine
   :alt: PyPI - Version

.. |Python Version| image:: https://img.shields.io/pypi/pyversions/djangorestframework-simplejwt-mongoengine
   :target: https://github.com/ngocngoan/djangorestframework-simplejwt-mongoengine/blob/main/LICENSE
   :alt: Python Version

.. |Django Version| image:: https://img.shields.io/pypi/frameworkversions/django/djangorestframework-simplejwt-mongoengine
   :target: https://github.com/django
   :alt: Django Version

.. |GitHub Actions| image:: https://img.shields.io/github/actions/workflow/status/ngocngoan/djangorestframework-simplejwt-mongoengine/test.yaml
   :target: https://github.com/ngocngoan/djangorestframework-simplejwt-mongoengine/actions
   :alt: GitHub Actions Workflow Status

.. |Code Style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black Format

.. |License| image:: https://img.shields.io/github/license/ngocngoan/djangorestframework-simplejwt-mongoengine
   :target: https://github.com/ngocngoan/djangorestframework-simplejwt-mongoengine/blob/main/LICENSE
   :alt: Repository License


A JSON Web Token authentication plugin for the `Django REST Framework
<http://www.django-rest-framework.org/>`__.

-------------------------------------------------------------------------------

Simple JWT MongoEngine provides a JSON Web Token authentication backend for the Django REST
Framework. It is re-written from `Simple JWT <https://github.com/jazzband/djangorestframework-simplejwt>`__.
It aims to cover the most common use cases of JWTs by offering a
conservative set of default features.  It also aims to be easily extensible in
case a desired feature is not present.

Contents
--------

.. toctree::
    :maxdepth: 3

    getting_started
    settings
    customizing_token_claims
    creating_tokens_manually
    token_types
    blacklist_app
    stateless_user_authentication
    rest_framework_simplejwt_mongoengine


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
