from django.conf import settings
from django.test.signals import setting_changed
from rest_framework_simplejwt.settings import DEFAULTS, IMPORT_STRINGS, APISettings

USER_SETTINGS = getattr(settings, "SIMPLE_JWT_MONGOENGINE", None)

DEFAULTS.update(
    {
        "VERIFYING_KEY": "",
        "JSON_ENCODER": None,
        "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt_mongoengine.authentication.default_user_authentication_rule",
        "TOKEN_USER_CLASS": "rest_framework_simplejwt_mongoengine.models.TokenUser",
        "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt_mongoengine.tokens.AccessToken",),
        "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt_mongoengine.serializers.TokenObtainPairSerializer",
        "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt_mongoengine.serializers.TokenRefreshSerializer",
        "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt_mongoengine.serializers.TokenVerifySerializer",
        "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt_mongoengine.serializers.TokenBlacklistSerializer",
        "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt_mongoengine.serializers.TokenObtainSlidingSerializer",  # noqa: E501
        "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt_mongoengine.serializers.TokenRefreshSlidingSerializer",  # noqa: E501
    }
)

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):  # pragma: no cover
    global api_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "SIMPLE_JWT_MONGOENGINE":
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)
