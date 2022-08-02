.. _getting_started:

Getting started
===============

Requirements
------------

* Python (3.8, 3.9, 3.10)
* Django (3.2, 4.0)
* Django REST Framework (3.11, 3.12, 3.13)
* `MongoEngine`_ (0.20, 0.21, 0.22, 0.23, 0.24)
* `Django MongoEngine`_ (0.5)
* `Simple JWT`_ 4.7

.. _MongoEngine: https://mongoengine-odm.readthedocs.io
.. _Django MongoEngine: https://github.com/MongoEngine/django-mongoengine
.. _Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io


Installation
------------

Simple JWT MongoEngine can be installed with pip::

  pip install djangorestframework-simplejwt-mongoengine

Then, your django project must be configured to use the library.  In
``settings.py``, add
``rest_framework_simplejwt_mongoengine.authentication.JWTAuthentication`` to the list of
authentication classes:

.. code-block:: python

  REST_FRAMEWORK = {
      ...
      'DEFAULT_AUTHENTICATION_CLASSES': (
          ...
          'rest_framework_simplejwt_mongoengine.authentication.JWTAuthentication',
      )
      ...
  }

Also, in your root ``urls.py`` file (or any other url config), include routes
for Simple JWT MongoEngine's ``TokenObtainPairView`` and ``TokenRefreshView`` views:

.. code-block:: python

  from rest_framework_simplejwt_mongoengine.views import (
      TokenObtainPairView,
      TokenRefreshView,
  )

  urlpatterns = [
      ...
      path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      ...
  ]

You can also include a route for Simple JWT MongoEngine's ``TokenVerifyView`` if you wish to
allow API users to verify HMAC-signed tokens without having access to your
signing key:

.. code-block:: python
  # add `TokenVerifyView` to your import

  from rest_framework_simplejwt_mongoengine.views import TokenVerifyView

  # and define it in your `urlpatterns`
  urlpatterns = [
      ...
      path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
      ...
  ]

If you wish to use localizations/translations, simply add
``rest_framework_simplejwt_mongoengine`` to ``INSTALLED_APPS``.

.. code-block:: python

  INSTALLED_APPS = [
      ...
      'rest_framework_simplejwt_mongoengine',
      ...
  ]


Usage
-----

To verify that Simple JWT MongoEngine is working, you can use curl to issue a couple of
test requests:

.. code-block:: bash

  curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
    http://localhost:8000/api/token/

  ...
  {
    "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
    "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
  }

You can use the returned access token to prove authentication for a protected
view:

.. code-block:: bash

  curl \
    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
    http://localhost:8000/api/some-protected-view/

When this short-lived access token expires, you can use the longer-lived
refresh token to obtain another access token:

.. code-block:: bash

  curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
    http://localhost:8000/api/token/refresh/

  ...
  {"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNTY3LCJqdGkiOiJjNzE4ZTVkNjgzZWQ0NTQyYTU0NWJkM2VmMGI0ZGQ0ZSJ9.ekxRxgb9OKmHkfy-zs1Ro_xs1eMLXiR17dIDBVxeT-w"}
