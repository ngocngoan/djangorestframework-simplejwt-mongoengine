.. _settings:

Settings
========

Some of Simple JWT MongoEngine's behavior can be customized through settings variables in
``settings.py``.

All Simple JWT MongoEngine's settings are the same as Simple JWT's settings except for 2 different entries:

.. code-block:: python

    # Django project settings.py

    ...

    SIMPLE_JWT_MONGOENGINE = {
        ...
        'TOKEN_USER_CLASS': ('rest_framework_simplejwt_mongoengine.models.TokenUser',),
        'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt_mongoengine.tokens.AccessToken',),
    }

Above, the default values for these settings are shown.

To see all the settings and their meanings, please refer to: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
