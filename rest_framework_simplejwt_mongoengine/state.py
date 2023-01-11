from .backends import TokenBackend
from .settings import api_settings
from .utils import drf_simplejwt_version

token_backend = (
    TokenBackend(api_settings.ALGORITHM, api_settings.SIGNING_KEY, api_settings.VERIFYING_KEY, api_settings.AUDIENCE, api_settings.ISSUER)
    if "4.7" in drf_simplejwt_version
    else TokenBackend(
        api_settings.ALGORITHM,
        api_settings.SIGNING_KEY,
        api_settings.VERIFYING_KEY,
        api_settings.AUDIENCE,
        api_settings.ISSUER,
        api_settings.JWK_URL,
        api_settings.LEEWAY,
        api_settings.JSON_ENCODER,
    )
)
