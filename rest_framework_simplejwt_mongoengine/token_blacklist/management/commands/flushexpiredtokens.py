from django.core.management.base import BaseCommand

from rest_framework_simplejwt_mongoengine.utils import aware_utcnow, microseconds_to_milliseconds

from ...models import OutstandingToken


class Command(BaseCommand):
    help = "Flushes any expired tokens in the outstanding token list"

    def handle(self, *args, **kwargs) -> None:
        OutstandingToken.objects.filter(expires_at__lte=microseconds_to_milliseconds(aware_utcnow())).delete()
