from datetime import timedelta
from typing import Union

import jwt
from django.utils.translation import gettext_lazy as _
from jwt import InvalidAlgorithmError, InvalidTokenError
from rest_framework_simplejwt.backends import TokenBackend as SimpleJwtTokenBackend
from rest_framework_simplejwt.exceptions import TokenBackendError
from rest_framework_simplejwt.utils import format_lazy

from .utils import drf_simplejwt_version

try:
    from jwt import PyJWKClient

    JWK_CLIENT_AVAILABLE = True
except ImportError:
    JWK_CLIENT_AVAILABLE = False


class TokenBackend(SimpleJwtTokenBackend):
    def __init__(
        self,
        algorithm,
        signing_key=None,
        verifying_key="",
        audience=None,
        issuer=None,
        jwk_url: str = None,
        # leeway=0,
        leeway: Union[float, int, timedelta] = None,
    ):
        if "4.7" in drf_simplejwt_version:
            super().__init__(algorithm, signing_key, verifying_key, audience, issuer)
        else:
            super().__init__(algorithm, signing_key, verifying_key, audience, issuer, jwk_url, leeway)

        if JWK_CLIENT_AVAILABLE:
            self.jwks_client = PyJWKClient(jwk_url) if jwk_url else None
        else:
            self.jwks_client = None

    def get_leeway(self) -> timedelta:
        leeway = getattr(self, "leeway", None)

        if leeway is None:
            return timedelta(seconds=0)
        elif isinstance(leeway, (int, float)):
            return timedelta(seconds=self.leeway)
        elif isinstance(leeway, timedelta):
            return self.leeway
        else:
            raise TokenBackendError(
                format_lazy(
                    _("Unrecognized type '{}', 'leeway' must be of type int, float or timedelta."),
                    type(self.leeway),
                )
            )

    def decode(self, token, verify=True):
        """
        Performs a validation of the given token and returns its payload
        dictionary.

        Raises a `TokenBackendError` if the token is malformed, if its
        signature check fails, or if its 'exp' claim indicates it has expired.
        """
        try:
            if "4.7" in drf_simplejwt_version:
                return jwt.decode(
                    token,
                    self.verifying_key,
                    algorithms=[self.algorithm],
                    verify=verify,
                    audience=self.audience,
                    issuer=self.issuer,
                    options={"verify_aud": self.audience is not None, "verify_signature": verify},
                )

            return jwt.decode(
                token,
                self.get_verifying_key(token),
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
                leeway=self.get_leeway(),
                options={
                    "verify_aud": self.audience is not None,
                    "verify_signature": verify,
                },
            )
        except InvalidAlgorithmError as ex:
            raise TokenBackendError(_("Invalid algorithm specified")) from ex
        except InvalidTokenError as ex:
            raise TokenBackendError(_("Token is invalid or expired")) from ex
