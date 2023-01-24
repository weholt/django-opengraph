def dummy_translator(request, instance):
    "A simple translator just mapping one property in the provided instance to a dictionary"
    return {
        property: hasattr(instance, property) and getattr(instance, property)
        for property in [
            "title",
            "description",
            "author",
            "keywords",
            "type",
            "locale",
            "twitter_card",
            "url",
            "image",
            "fb_admins",
            "fb_app_id",
            "site_name",
        ]
    }
