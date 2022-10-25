from django.conf import settings
from django.utils import timezone
from django_mongoengine.mongo_auth.managers import get_user_document
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer as SimpleJWTTokenObtainSerializer,
)
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer as SimpleJWTTokenRefreshSerializer,
)
from rest_framework_simplejwt.serializers import (
    TokenRefreshSlidingSerializer as SimpleJWTTokenRefreshSlidingSerializer,
)
from rest_framework_simplejwt.serializers import (
    TokenVerifySerializer as SimpleJWTTokenVerifySerializer,
)

from .settings import api_settings
from .tokens import RefreshToken, SlidingToken, UntypedToken
from .utils import drf_simplejwt_version

if api_settings.BLACKLIST_AFTER_ROTATION:
    from .token_blacklist.models import BlacklistedToken, OutstandingToken


class TokenObtainSerializer(SimpleJWTTokenObtainSerializer):
    username_field = get_user_document().USERNAME_FIELD
    token_class = None

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            self.user.last_login = timezone.now()
            self.user.save()

        return data


class TokenObtainSlidingSerializer(TokenObtainSerializer):
    token_class = SlidingToken

    def validate(self, attrs):
        data = super().validate(attrs)

        token = self.get_token(self.user)

        data["token"] = str(token)

        if api_settings.UPDATE_LAST_LOGIN:
            self.user.last_login = timezone.now()
            self.user.save()

        return data


class TokenRefreshSerializer(SimpleJWTTokenRefreshSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data["refresh"] = str(refresh)

        return data


class TokenRefreshSlidingSerializer(SimpleJWTTokenRefreshSlidingSerializer):
    token_class = SlidingToken

    def validate(self, attrs):
        token = self.token_class(attrs["token"])

        # Check that the timestamp in the "refresh_exp" claim has not
        # passed
        token.check_exp(api_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

        # Update the "exp" claim
        token.set_exp()

        return {"token": str(token)}


class TokenVerifySerializer(SimpleJWTTokenVerifySerializer):
    def validate(self, attrs):
        token = UntypedToken(attrs["token"])

        if (
            api_settings.BLACKLIST_AFTER_ROTATION
            and "rest_framework_simplejwt_mongoengine.token_blacklist"
            in settings.INSTALLED_APPS
        ):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(
                token__in=OutstandingToken.objects.filter(jti=jti)
            ).exists():
                raise ValidationError("Token is blacklisted")

        return {}


if drf_simplejwt_version in ["5.0.0", "5.1.0"]:
    from rest_framework_simplejwt.serializers import (
        TokenBlacklistSerializer as SimpleJWTTokenBlacklistSerializer,
    )

    class TokenBlacklistSerializer(SimpleJWTTokenBlacklistSerializer):
        token_class = RefreshToken

        def validate(self, attrs):
            refresh = self.token_class(attrs["refresh"])
            try:
                refresh.blacklist()
            except AttributeError:
                pass
            return {}
