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

        'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt_mongoengine.authentication.default_user_authentication_rule',
        'TOKEN_USER_CLASS': ('rest_framework_simplejwt_mongoengine.models.TokenUser',),
        'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt_mongoengine.tokens.AccessToken',),
    }

``AUTH_TOKEN_CLASSES``
----------------------

A list of dot paths to classes that specify the types of token that are allowed
to prove authentication.  More about this in the "Token types" section below.

``USER_AUTHENTICATION_RULE``
----------------------------

Callable to determine if the user is permitted to authenticate. This rule
is applied after a valid token is processed. The user object is passed
to the callable as an argument. The default rule is to check that the ``is_active``
flag is still ``True``. The callable must return a boolean, ``True`` if authorized,
``False`` otherwise resulting in a 401 status code.

``TOKEN_USER_CLASS``
--------------------

A stateless user object which is backed by a validated token. Used only for
the JWTStatelessUserAuthentication authentication backend. The value
is a dotted path to your subclass of ``rest_framework_simplejwt_mongoengine.models.TokenUser``,
which also is the default.

Above, the default values for these settings are shown.

To see all the settings and their meanings, please refer to: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
