import hashlib
import math
from calendar import timegm
from datetime import datetime, timezone
from typing import Callable

from django.conf import settings
from django.utils.functional import lazy


def get_md5_hash_password(password: str) -> str:
    """
    Returns MD5 hash of the given password
    """
    return hashlib.md5(password.encode()).hexdigest().upper()


def make_utc(dt: datetime) -> datetime:
    if settings.USE_TZ and dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt


def aware_utcnow() -> datetime:
    dt = datetime.now(tz=timezone.utc)
    if not settings.USE_TZ:
        dt = dt.replace(tzinfo=None)

    return dt


def datetime_to_epoch(dt: datetime) -> int:
    return timegm(dt.utctimetuple())


def datetime_from_epoch(ts: float) -> datetime:
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    if not settings.USE_TZ:
        dt = dt.replace(tzinfo=None)

    return dt


def format_lazy(s: str, *args, **kwargs) -> str:
    return s.format(*args, **kwargs)


format_lazy: Callable = lazy(format_lazy, str)


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
