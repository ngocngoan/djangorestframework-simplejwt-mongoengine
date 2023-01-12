=======
Changelog
=======

1.2.0 (2023-01-12)
------------------

* Python (3.8, 3.9, 3.10)
* Django (3.2, 4.0)
* Django REST Framework (3.11, 3.12, 3.13, 3.14)
* `MongoEngine`_ (0.20, 0.21, 0.22, 0.23, 0.24)
* `Django MongoEngine`_ (0.5)
* `Simple JWT`_ 4.7, 4.8, 5.0, 5.1, 5.2

.. _MongoEngine: https://mongoengine-odm.readthedocs.io
.. _Django MongoEngine: https://github.com/MongoEngine/django-mongoengine
.. _Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io

* Remove the JWTTokenUserAuthentication from the Experimental Features
* Fix leeway type error
* Add info on TokenBlacklistView to the docs
* Update JWTStatelessUserAuthentication docs
* Allow none jti claim token type clai
* Allow customizing token JSON encoding
* Optimize default_user_authentication_rule
* Add back support for PyJWT 1.7.1
* Make the token serializer configurable
* Add blacklist view to log out users
* Set default verifying key to empty str
* Add django simplejwt 5.2.2


1.1.0 (2022-08-08)
------------------

* Python (3.8, 3.9, 3.10)
* Django (3.2, 4.0)
* Django REST Framework (3.11, 3.12, 3.13, 3.14)
* `MongoEngine`_ (0.20, 0.21, 0.22, 0.23, 0.24)
* `Django MongoEngine`_ (0.5)
* `Simple JWT`_ 4.7, 4.8, 5.0

.. _MongoEngine: https://mongoengine-odm.readthedocs.io
.. _Django MongoEngine: https://github.com/MongoEngine/django-mongoengine
.. _Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io

* Add django simplejwt 5.0
* Drop support Python 3.7


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
