from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("djangorestframework_simplejwt_mongoengine")
except PackageNotFoundError:
    # package is not installed
    __version__ = None


__author__ = """Đỗ Ngọc Ngoạn (aka Ngoan Do)"""
__email__ = "ngocngoan060288@gmail.com"
