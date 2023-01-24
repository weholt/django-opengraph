from django.urls import path
from django.views.generic.base import TemplateView


class Post:
    title = "Title from an object"
    description = "Description from an object"
    keywords = "Keywords, from, an, object"
    author = "Author from an object"
    locale = "Locale from an object"
    twitter_card = "summary"
    url = "github.com"
    image = "https://picsum.photos/200/300"
    site_name = "Acme Inc"


class HomeView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post()
        return context


urlpatterns = [
    path("", HomeView.as_view()),
]
