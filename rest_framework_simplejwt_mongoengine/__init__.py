from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("rest_framework_simplejwt_mongoengine")
except PackageNotFoundError:
    # package is not installed
    __version__ = None
