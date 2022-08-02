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
    TokenVerifySerializer as SimpleJWTTokenVerifySerializer
)

from .settings import api_settings
from .tokens import RefreshToken, SlidingToken, UntypedToken

if api_settings.BLACKLIST_AFTER_ROTATION:
    from .token_blacklist.models import BlacklistedToken, OutstandingToken


class TokenObtainSerializer(SimpleJWTTokenObtainSerializer):
    username_field = get_user_document().USERNAME_FIELD


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

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
    @classmethod
    def get_token(cls, user):
        return SlidingToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        token = self.get_token(self.user)

        data["token"] = str(token)

        if api_settings.UPDATE_LAST_LOGIN:
            self.user.last_login = timezone.now()
            self.user.save()

        return data


class TokenRefreshSerializer(SimpleJWTTokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])

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
    def validate(self, attrs):
        token = SlidingToken(attrs["token"])

        # Check that the timestamp in the "refresh_exp" claim has not
        # passed
        token.check_exp(api_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

        # Update the "exp" claim
        token.set_exp()

        return {"token": str(token)}


class TokenVerifySerializer(SimpleJWTTokenVerifySerializer):
    def validate(self, attrs):
        token = UntypedToken(attrs['token'])

        if api_settings.BLACKLIST_AFTER_ROTATION:
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__in=OutstandingToken.objects.filter(jti=jti)).exists():
                raise ValidationError("Token is blacklisted")

        return {}
