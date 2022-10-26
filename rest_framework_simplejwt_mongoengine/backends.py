from rest_framework_simplejwt.backends import TokenBackend as SimpleJwtTokenBackend

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
        leeway=0,
    ):
        if drf_simplejwt_version in ["4.7.0", "4.7.1", "4.7.2"]:
            super().__init__(algorithm, signing_key, verifying_key, audience, issuer)
        else:
            super().__init__(
                algorithm, signing_key, verifying_key, audience, issuer, jwk_url, leeway
            )

        if JWK_CLIENT_AVAILABLE:
            self.jwks_client = PyJWKClient(jwk_url) if jwk_url else None
        else:
            self.jwks_client = None
        self.leeway = leeway
