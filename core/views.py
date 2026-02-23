from django.shortcuts import render
from posts.models import Post
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from posts.forms import COUNTRIES


def home(request):
    query = request.GET.get("q")
    selected_country = request.GET.get("country")
    posts = Post.objects.all().order_by("-created_at")

    if query:
        posts = (
            posts.annotate(
                similarity=Greatest(
                    TrigramSimilarity("country", query),
                    TrigramSimilarity("place", query),
                )
            )
            .filter(
                Q(country__icontains=query) |
                Q(place__icontains=query) |
                Q(similarity__gte=0.2)
            )
            .order_by("-similarity", "-created_at")
            .distinct()
        )

    if selected_country:
        posts = posts.filter(country=selected_country)

    return render(request, "core/home.html", {
        "posts": posts,
        "query": query,
        "countries": [country[0] for country in COUNTRIES],
        "selected_country": selected_country,
    })

