from rest_framework_simplejwt.backends import TokenBackend

from .settings import api_settings

token_backend = TokenBackend(api_settings.ALGORITHM, api_settings.SIGNING_KEY,
                             api_settings.VERIFYING_KEY, api_settings.AUDIENCE, api_settings.ISSUER)
