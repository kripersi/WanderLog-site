from django.shortcuts import render
from posts.models import Post
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest


def home(request):
    query = request.GET.get("q")
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

    return render(request, "core/home.html", {
        "posts": posts,
        "query": query
    })

