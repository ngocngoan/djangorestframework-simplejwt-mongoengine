import math
from calendar import timegm
from datetime import datetime, timezone

from django.conf import settings
from django.utils.functional import lazy
from django.utils.timezone import is_naive, make_aware
from pkg_resources import get_distribution

drf_simplejwt_version = get_distribution("djangorestframework_simplejwt").version


def make_utc(dt):
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=timezone.utc)

    return dt


def aware_utcnow():
    return make_utc(datetime.utcnow())


def datetime_to_epoch(dt):
    return timegm(dt.utctimetuple())


def datetime_from_epoch(ts):
    return make_utc(datetime.utcfromtimestamp(ts))


def format_lazy(s, *args, **kwargs):
    return s.format(*args, **kwargs)


format_lazy = lazy(format_lazy, str)


def microseconds_to_milliseconds(date_time):
    """
    Because Mongodb only stores Date data type to milliseconds
    while Python stores data type datetime to microseconds.
    So this function converts data to be compatible with MongoDB

    Reference: https://docs.mongodb.com/manual/reference/method/Date/#behavior

    :param date_time: instance of `datetime` class
    :return: instance of `datetime` class with milliseconds
    """
    milliseconds = math.floor(date_time.microsecond / 1000) * 1000
    return date_time.replace(microsecond=milliseconds)
