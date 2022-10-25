def pytest_configure():
    from django.conf import settings

    MIDDLEWARE = (
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    )

    settings.configure(
        ALLOWED_HOSTS=["*"],
        DEBUG=True,
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        MONGODB_DATABASES={
            "default": {
                "host": "127.0.0.1",
                "port": 27017,
                "name": "test_simplejwt",
                "username": "admin",
                "password": "SimpleJWT_MongoEngine",
                "tz_aware": True,
                "authentication_mechanism": "SCRAM-SHA-1",
                "authentication_source": "admin",
                "uuidrepresentation": "standard",
                "readpreference": "primary",
                "ssl": False,
                "tls": False,
            },
            "other": {
                "host": "127.0.0.1",
                "port": 27017,
                "name": "test_other_simplejwt",
                "username": "admin",
                "password": "SimpleJWT_MongoEngine",
                "tz_aware": True,
                "authentication_mechanism": "SCRAM-SHA-1",
                "authentication_source": "admin",
                "uuidrepresentation": "standard",
                "readpreference": "primary",
                "ssl": False,
                "tls": False,
            },
        },
        SESSION_ENGINE="django_mongoengine.sessions",
        SESSION_SERIALIZER="django_mongoengine.sessions.BSONSerializer",
        AUTH_USER_MODEL="mongo_auth.MongoUser",
        SITE_ID=1,
        SECRET_KEY="not very secret in tests",
        USE_I18N=True,
        STATIC_URL="/static/",
        ROOT_URLCONF="tests.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
            },
        ],
        MIDDLEWARE=MIDDLEWARE,
        MIDDLEWARE_CLASSES=MIDDLEWARE,
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "django_mongoengine",
            "django_mongoengine.mongo_auth",
            "django_mongoengine.mongo_admin",
            "rest_framework",
            "rest_framework_simplejwt_mongoengine",
            "rest_framework_simplejwt_mongoengine.token_blacklist",
            "tests",
        ),
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
        TIME_ZONE="UTC",
        LANGUAGE_CODE="en-us",
        USE_TZ=True,
    )

    try:
        import django

        django.setup()
    except AttributeError:
        pass
