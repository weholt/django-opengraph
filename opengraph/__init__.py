__all__ = ("VERSION",)

try:
    VERSION = __import__("pkg_resources").get_distribution("django-opengraph").version
except Exception as ex:
    VERSION = "unknown"
