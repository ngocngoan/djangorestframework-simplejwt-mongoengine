from django import VERSION

if VERSION < (3, 2):
    default_app_config = 'rest_framework_simplejwt_mongoengine.token_blacklist.apps.TokenBlacklistConfig'
