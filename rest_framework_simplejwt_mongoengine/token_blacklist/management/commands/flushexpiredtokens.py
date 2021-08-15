from django.core.management.base import BaseCommand
from rest_framework_simplejwt.utils import aware_utcnow

from rest_framework_simplejwt_mongoengine.utils import microseconds_to_milliseconds

from ...models import OutstandingToken


class Command(BaseCommand):
    help = "Flushes any expired tokens in the outstanding token list"

    def handle(self, *args, **kwargs):
        OutstandingToken.objects.filter(expires_at__lte=microseconds_to_milliseconds(aware_utcnow())).delete()
