from django.conf import settings
from django.utils import timezone
from django_mongoengine import document
from django_mongoengine.mongo_auth.managers import get_user_document
from django_mongoengine.queryset import QuerySetManager
from mongoengine import fields, queryset

User = get_user_document()


class OutstandingTokenManager(QuerySetManager):
    pass


class OutstandingToken(document.Document):
    user = fields.ReferenceField(User, reverse_delete_rule=queryset.NULLIFY, null=True)

    jti = fields.StringField(unique=True, max_length=255)
    token = fields.StringField()

    created_at = fields.DateTimeField(default=timezone.now, null=True)
    expires_at = fields.DateTimeField()

    objects = OutstandingTokenManager()

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = (
            "rest_framework_simplejwt_mongoengine.token_blacklist"
            not in settings.INSTALLED_APPS
        )
        ordering = ("user",)

    def __str__(self):
        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )


class BlacklistedTokenManager(QuerySetManager):
    pass


class BlacklistedToken(document.Document):
    token = fields.ReferenceField(
        OutstandingToken, reverse_delete_rule=queryset.CASCADE
    )

    blacklisted_at = fields.DateTimeField(default=timezone.now)

    objects = BlacklistedTokenManager()

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = (
            "rest_framework_simplejwt_mongoengine.token_blacklist"
            not in settings.INSTALLED_APPS
        )

    def __str__(self):
        return f"Blacklisted token for {self.token.user}"
