from django.utils.translation import gettext_lazy as _
from django_mongoengine.apps import DjangoMongoEngineConfig


class TokenBlacklistConfig(DjangoMongoEngineConfig):
    name = "rest_framework_simplejwt_mongoengine.token_blacklist"
    verbose_name = _("Token Blacklist")
    default_auto_field = "django.db.models.BigAutoField"
