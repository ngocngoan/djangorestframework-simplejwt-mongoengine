=========
Changelog
=========


1.3.0 (2024-05-30)
------------------

* Python (3.8, 3.9, 3.10, 3.11)
* Django (3.2, 4.1, 4.2)
* Django REST Framework (3.12, 3.13, 3.14, 3.15)
* `Django MongoEngine`_ (0.5.4, 0.5.5, 0.5.6)

* Add support Django 4.1 and 4.2
* Add support Django REST Framework 3.15
* update features that includes `Simple JWT`_ 5.3.x
* Drop `Simple JWT`_ as dependency


1.2.1 (2023-01-18)
------------------

* Python (3.8, 3.9, 3.10, 3.11)
* Django (3.2, 4.0)
* Django REST Framework (3.11, 3.12, 3.13, 3.14)
* `MongoEngine`_ (0.20, 0.21, 0.22, 0.23, 0.24)
* `Django MongoEngine`_ (0.5)
* `Simple JWT`_ 4.7, 4.8, 5.0, 5.1, 5.2

* Add support for Python 3.11
* update package requires that includes `Simple JWT`_ 5.2


1.2.0 (2023-01-12)
------------------

* Python (3.8, 3.9, 3.10)
* Django (3.2, 4.0)
* Django REST Framework (3.11, 3.12, 3.13, 3.14)
* `MongoEngine`_ (0.20, 0.21, 0.22, 0.23, 0.24)
* `Django MongoEngine`_ (0.5)
* `Simple JWT`_ 4.7, 4.8, 5.0, 5.1

* Remove the JWTTokenUserAuthentication from the Experimental Features
* Fix leeway type error
* Add info on TokenBlacklistView to the docs
* Update JWTStatelessUserAuthentication docs
* Allow none jti claim token type clai
* Allow customizing token JSON encoding
* Optimize default_user_authentication_rule
* Add back support for `PyJWT`_ 1.7.1
* Make the token serializer configurable
* Add blacklist view to log out users
* Set default verifying key to empty str
* Add support `Simple JWT`_ 5.1 and 5.2.x


1.1.0 (2022-08-08)
------------------

* Python (3.8, 3.9, 3.10)
* Django (3.2, 4.0)
* Django REST Framework (3.11, 3.12, 3.13, 3.14)
* `MongoEngine`_ (0.20, 0.21, 0.22, 0.23, 0.24)
* `Django MongoEngine`_ (0.5)
* `Simple JWT`_ 4.7, 4.8, 5.0

* Add support `Simple JWT`_ 5.0
* Drop support Python 3.7
* Drop support `Simple JWT`_ 4.6


1.0.0 (2021-08-20)
------------------

* First release
* Python (3.7, 3.8, 3.9)
* Django (3.2)
* Django REST Framework (3.11, 3.12)
* `MongoEngine`_ (0.20, 0.21, 0.22, 0.23)
* `Django MongoEngine`_ (0.4.6)
* `Simple JWT`_ 4.6 with `PyJWT`_ 1.7.1 or `Simple JWT`_ 4.7 with `PyJWT`_ 2.1.0

.. _MongoEngine: https://mongoengine-odm.readthedocs.io
.. _Django MongoEngine: https://github.com/MongoEngine/django-mongoengine
.. _Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io
.. _PyJWT: https://pyjwt.readthedocs.io
