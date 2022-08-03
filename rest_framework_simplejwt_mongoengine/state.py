from rest_framework_simplejwt.backends import TokenBackend

from .settings import api_settings
from .utils import drf_simplejwt_version

if drf_simplejwt_version in ["4.7.0", "4.7.1", "4.7.2"]:
    token_backend = TokenBackend(
        api_settings.ALGORITHM,
        api_settings.SIGNING_KEY,
        api_settings.VERIFYING_KEY,
        api_settings.AUDIENCE,
        api_settings.ISSUER,
    )
else:
    token_backend = TokenBackend(
        api_settings.ALGORITHM,
        api_settings.SIGNING_KEY,
        api_settings.VERIFYING_KEY,
        api_settings.AUDIENCE,
        api_settings.ISSUER,
        api_settings.JWK_URL,
        api_settings.LEEWAY,
    )
