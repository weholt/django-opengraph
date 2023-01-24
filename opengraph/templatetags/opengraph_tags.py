from typing import List

from django import template
from django.conf import settings

from opengraph.object_translator import dummy_translator

# from django.core.validators import EMPTY_VALUES


register = template.Library()


@register.inclusion_tag("opengraph/base.html", takes_context=True)
def opengraph(context, *args, **kwargs):
    return get_opengraph_attributes(context, kwargs)


@register.inclusion_tag("opengraph/base.html", takes_context=True)
def opengraph_from_object(context, instance):
    request = context["request"]
    config = getattr(settings, "OPENGRAPH_CONFIG", {})
    object_translators = config.get("OBJECT_TRANSLATOR", {})
    specific_translator = (
        object_translators.get(instance.__class__.__name__, None) or dummy_translator
    )
    return get_opengraph_attributes(context, specific_translator(request, instance))


def get_opengraph_attributes(context, kwargs):
    request = context["request"]
    config = getattr(settings, "OPENGRAPH_CONFIG", {})

    graph = {
        "title": kwargs.get("title", config.get("DEFAULT_TITLE")),
        "description": kwargs.get("description", config.get("DEFAULT_DESCRIPTION")),
        "keywords": kwargs.get("keywords", config.get("DEFAULT_KEYWORDS")),
        "author": kwargs.get("author", config.get("DEFAULT_AUTHOR")),
        "type": kwargs.get("type", config.get("DEFAULT_TYPE", "website")),
        "locale": kwargs.get("locale", config.get("DEFAULT_LOCALE", "en")),
        "twitter_card": kwargs.get("twitter_card", config.get("DEFAULT_TWITTER_CARD")),
        "url": kwargs.get("url", request.build_absolute_uri()),
        "image": kwargs.get("image"),
    }

    graph["fb_admins"] = kwargs.get("fb_admins", config.get("FB_ADMINS", None))
    graph["fb_app_id"] = kwargs.get("fb_app_id", config.get("FB_APP_ID", None))
    graph["site_name"] = kwargs.get("site_name", config.get("SITE_NAME", None))
    default_image = normalize_image_url(request, config.get("DEFAULT_IMAGE", None))

    images = []
    if default_image is not None:
        images.append(default_image)
    image = kwargs.get("image", None)
    if image in EMPTY_VALUES:
        image = None
    if isinstance(image, List):
        images = [normalize_image_url(request, img) for img in image]
    elif isinstance(
        image, str
    ):  # or isinstance(image, SafeUnicode) or isinstance(image, unicode):
        images = [normalize_image_url(request, image)]
    graph["images"] = images
    return graph


def normalize_image_url(request, image):
    if image is None or image[:4] == "http":
        return image
    protocol = "http"
    if request.is_secure():
        protocol = "https"
    if image[:2] == "//":
        return "%s:%s" % (protocol, image)
    host = request.get_host()
    return "%s://%s%s" % (protocol, host, image)
