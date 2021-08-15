from datetime import timedelta

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.tokens import Token as SimpleJWTToken
from rest_framework_simplejwt.utils import aware_utcnow, datetime_from_epoch

from .settings import api_settings
from .token_blacklist.models import BlacklistedToken, OutstandingToken
from .utils import microseconds_to_milliseconds


class Token(SimpleJWTToken):
    def __init__(self, token=None, verify=True):
        """
        !!!! IMPORTANT !!!! MUST raise a TokenError with a user-facing error
        message if the given token is invalid, expired, or otherwise not safe
        to use.
        """
        if self.token_type is None or self.lifetime is None:
            raise TokenError(_("Cannot create token with no type or lifetime"))

        self.token = token
        self.current_time = microseconds_to_milliseconds(aware_utcnow())

        # Set up token
        if token is not None:
            # An encoded token was provided
            token_backend = self.get_token_backend()

            # Decode token
            try:
                self.payload = token_backend.decode(token, verify=verify)
            except TokenBackendError:
                raise TokenError(_("Token is invalid or expired"))

            if verify:
                self.verify()
        else:
            # New token.  Skip all the verification steps.
            self.payload = {api_settings.TOKEN_TYPE_CLAIM: self.token_type}

            # Set "exp" claim with default value
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)

            # Set "jti" claim
            self.set_jti()

    def __str__(self):
        """
        Signs and returns a token as a base64 encoded string.
        """
        return self.get_token_backend().encode(self.payload)

    @classmethod
    def for_user(cls, user):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        user_id = getattr(user, api_settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        token[api_settings.USER_ID_CLAIM] = user_id

        return token

    _token_backend = None

    def get_token_backend(self):
        if self._token_backend is None:
            self._token_backend = import_string("rest_framework_simplejwt_mongoengine.state.token_backend")
        return self._token_backend


class BlacklistMixin:
    """
    If the `rest_framework_simplejwt_mongoengine.token_blacklist` app was configured to be
    used, tokens created from `BlacklistMixin` subclasses will insert
    themselves into an outstanding token list and also check for their
    membership in a token blacklist.
    """

    if "rest_framework_simplejwt_mongoengine.token_blacklist" in settings.INSTALLED_APPS:

        def verify(self, *args, **kwargs):
            self.check_blacklist()

            super().verify(*args, **kwargs)

        def check_blacklist(self):
            """
            Checks if this token is present in the token blacklist.  Raises
            `TokenError` if so.
            """
            jti = self.payload[api_settings.JTI_CLAIM]

            if BlacklistedToken.objects.filter(token__in=OutstandingToken.objects.filter(jti=jti)).exists():
                raise TokenError(_("Token is blacklisted"))

        def blacklist(self):
            """
            Ensures this token is included in the outstanding token list and
            adds it to the blacklist.
            """
            jti = self.payload[api_settings.JTI_CLAIM]
            exp = self.payload["exp"]

            # Ensure outstanding token exists with given jti
            token, _ = OutstandingToken.objects.get_or_create(
                jti=jti,
                defaults={
                    "token": str(self),
                    "expires_at": datetime_from_epoch(exp),
                },
            )

            try:
                blacklist_token = BlacklistedToken.objects.get(token=token)
            except BlacklistedToken.DoesNotExist:
                blacklist_token = BlacklistedToken.objects.create(token=token)

            return blacklist_token

        @classmethod
        def for_user(cls, user):
            """
            Adds this token to the outstanding token list.
            """
            token = super().for_user(user)

            jti = token[api_settings.JTI_CLAIM]
            exp = token["exp"]

            OutstandingToken.objects.create(
                user=user,
                jti=jti,
                token=str(token),
                created_at=token.current_time,
                expires_at=datetime_from_epoch(exp),
            )

            return token


class SlidingToken(BlacklistMixin, Token):
    token_type = "sliding"
    lifetime = api_settings.SLIDING_TOKEN_LIFETIME

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.token is None:
            # Set sliding refresh expiration claim if new token
            self.set_exp(
                api_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM,
                from_time=self.current_time,
                lifetime=api_settings.SLIDING_TOKEN_REFRESH_LIFETIME,
            )


class RefreshToken(BlacklistMixin, Token):
    token_type = "refresh"
    lifetime = api_settings.REFRESH_TOKEN_LIFETIME
    no_copy_claims = (
        api_settings.TOKEN_TYPE_CLAIM,
        "exp",
        # Both of these claims are included even though they may be the same.
        # It seems possible that a third party token might have a custom or
        # namespaced JTI claim as well as a default "jti" claim.  In that case,
        # we wouldn't want to copy either one.
        api_settings.JTI_CLAIM,
        "jti",
    )

    @property
    def access_token(self):
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        access = AccessToken()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access


class AccessToken(Token):
    token_type = "access"
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME


class UntypedToken(Token):
    token_type = "untyped"
    lifetime = timedelta(seconds=0)

    def verify_token_type(self):
        """
        Untyped tokens do not verify the "token_type" claim.  This is useful
        when performing general validation of a token's signature and other
        properties which do not relate to the token's intended use.
        """
        pass
