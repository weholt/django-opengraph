# OpenGraph App for Django >= 4.x

Note! This is a fork of the https://github.com/leveille/django-opengraph repository, which lacked support
for audio and video tags. I've also included support for getting properties from an object instance, using a
"object translator". The translator function can be specified in settings.py and be customized to your hearts content.

Adds HTML Meta tags for OpenGraph support.

* [OpenGraph](http://ogp.me/)
* [Facebook OpenGraph](https://developers.facebook.com/docs/opengraph/property-types/)
    
## Installation

```
pip install -e git+git://github.com/weholt/django-opengraph.git#egg=opengraph
```

## Upgrade

```
pip install -U -e git+git://github.com/weholt/django-opengraph.git#egg=opengraph
```

## Usage

### Optional Configuration

1. Add opengraph to your settings.py INSTALLED_APPS list
2. There are a few configuration options to opengraph that can be placed in an OPTIONAL dictionary called OPENGRAPH_CONFIG in settings.py.

```python
OPENGRAPH_CONFIG = {
    'FB_ADMINS': '###',
    'FB_APP_ID': '###',
    'DEFAULT_IMAGE': '%sdefault/image.png' % STATIC_URL,
    'SITE_NAME': 'Your Site Name',
}
```

* `FB_ADMINS`: __optional__
  Something here

* `FB_APP_ID`: __optional__
  Something here

* `DEFAULT_IMAGE`: __optional__
  Default image to use in the open graph.

* `SITE_NAME`:
  Name of your site

### Loading Template Tags

1. Load the `opengraph_tags` custom tags
2. Call the `opengraph` tag, passing in the appropriate parameters

Assume the following configuration:

```python
OPENGRAPH_CONFIG = {
    "FB_ADMINS": "123",
    "FB_APP_ID": "456",
    "SITE_NAME": "National Priorities Project",
    "DEFAULT_IMAGE": "%simages/default.png" % STATIC_URL,
    "DEFAULT_TITLE": "Default title",
    "DEFAULT_DESCRIPTION": "Default description",
    "DEFAULT_KEYWORDS": "Default, Keywords, Goes, Here",
    "DEFAULT_AUTHOR": "Your name",
    "DEFAULT_TYPE": "website",
    "DEFAULT_URL": "Default url",
    "DEFAULT_LOCALE": "en_EN",
    "DEFAULT_TWITTER_CARD": "summary" | "summary_large_image" | "app" | "player"
}
```

```html
{% load opengraph_tags %}
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Django OpenGraph Example</title>
        {% opengraph title='Django OpenGraph Example' description='This is a test' image="http://site.tld/image.png" %}
    </head>
    <body></body>
</html>
```

The result, including the use of the OPENGRAPH_CONFIG options defined above, would be:

```html
<meta property="fb:admins" content="123">
<meta property="fb:app_id" content="456">
<meta property="og:title" content="Django OpenGraph Example">
<meta property="og:type" content="website">
<meta property="og:url" content="http://127.0.0.1:8000/">
<meta property="og:image" content="http://site.tld/image.png">
<meta property="og:description" content="This is a test">
<meta property="og:site_name" content="Your Site Name">
```

## OpenGraph Tag

```
{% opengraph fb_admins="" fb_app_id="" site_name="" type="" url="" title="" description="" image="" %}
```

* `fb_admins`: __optional__  
  The ID (or comma-separated list for properties that can accept multiple IDs) of an app, person using the app, or Page Graph API object.

* `fb_app_id`: __optional__  
  The ID of your Facebook Application

* `site_name`: __required if not defined by `SITE_NAME` in OPENGRAPH_CONFIG__  
  If your object is part of a larger web site, the name which should be displayed for the overall site. e.g., "IMDb"

* `type`: __optional__  
  The type of your object, e.g., "video.movie".  
  Defaults to `website`

* `url`: __optional__  
  The canonical URL of your object that will be used as its permanent ID in the graph, e.g., "http://www.imdb.com/title/tt0117500/".
  Defaults to `request.build_absolute_url()`

* `title`: __required__  
  The title of your object as it should appear within the graph, e.g., "The Rock".  Title should be concise as it may be truncated depending on where it is used (in the NewsFeed, etc).

* `description`: __optional__  
  A one to two sentence description of your object.  Description should be concise as it may be truncated depending on where it is used (in the NewsFeed, etc).

* `image`: __required if not defined by `DEFAULT_IMAGE` in OPENGRAPH_CONFIG__  
  An image URL which should represent your object within the graph.  
  Defaults to `DEFAULT_IMAGE` if defined in `OPENGRAPH_CONFIG`

## Opengraph-from-object Tag

```
{% opengraph_from_object instance %}
```
Will try to look for properties on the instance mapping to the ones required. You can also specify your own object translator to do the mapping manually, if it isn't 1:1.

The callable takes two arguments, the request object and the instance itself. It should return a dictionary.

For instance, when creating a blog in Wagtail, you might write something like this:

```
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    cover = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    .... More fields here ...
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)    
```

And in your settings you map your translator to your object class:

```
def blogpage_translator(request, instance):
    return {
      "title": instance.title,
      "description": instance.intro,
      "image": instance.cover.url,
      "keywords": ", ".join([tag.name for tag in instance.tags.all()])
    }

OPENGRAPH_CONFIG = {
  ...    
  "OBJECT_TRANSLATOR": {"BlogPage": blogpage_translator},
}
```

In your template, you can now just pass the page instance to the opengraph_from_object-tag, and it will map the properties for you. Like so:

```
{% load opengraph_tags %}

{% block extra_head %}
{% image page.cover original as tmp_photo %}
{% with photo_url=tmp_photo.url %}
{% opengraph_from_object page image=photo_url %}
{% endwith %}
{% endblock %}
```

A more 
## Version history

0.0.6 : 
 - base version

0.0.7 : 
 - rewrite to work with Python >= 3.8 and Django >= 4.x
 - new template tag taking an instance as parameter

## Known issues

The generated html is a bit verbose and contain a lot of whitespace if not all the properties are being used. 
I'm working on fixing this, but any information about how to avoid this is highly appreciated. Email me at thomas@weholt.org.