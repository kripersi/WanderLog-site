from django.shortcuts import render
from posts.models import Post
from django.db.models import Q


def home(request):
    query = request.GET.get("q")
    posts = Post.objects.all().order_by("-created_at")

    if query:
        posts = posts.filter(
            Q(country__icontains=query) |
            Q(place__icontains=query)
        ).distinct()

    return render(request, "core/home.html", {
        "posts": posts,
        "query": query
    })

