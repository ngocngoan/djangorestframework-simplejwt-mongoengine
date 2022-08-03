import math
from pkg_resources import get_distribution


drf_simplejwt_version = get_distribution("djangorestframework_simplejwt").version


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
