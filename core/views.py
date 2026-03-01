from django.shortcuts import render
from posts.models import Post
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from posts.forms import COUNTRIES
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


def _filtered_posts(query, selected_country):
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
                Q(country__icontains=query)
                | Q(place__icontains=query)
                | Q(similarity__gte=0.2)
            )
            .order_by("-similarity", "-created_at")
            .distinct()
        )

    if selected_country:
        posts = posts.filter(country=selected_country)

    return posts


def home(request):
    query = request.GET.get("q")
    selected_country = request.GET.get("country")
    posts = _filtered_posts(query, selected_country)
    paginator = Paginator(posts, 12)
    page_obj = paginator.get_page(request.GET.get("page") or 1)

    return render(request, "core/home.html", {
        "posts": page_obj.object_list,
        "page_obj": page_obj,
        "query": query,
        "countries": [country[0] for country in COUNTRIES],
        "selected_country": selected_country,
    })


def feed(request):
    query = request.GET.get("q")
    selected_country = request.GET.get("country")
    posts = _filtered_posts(query, selected_country)
    paginator = Paginator(posts, 12)
    page_obj = paginator.get_page(request.GET.get("page") or 1)
    html = render_to_string(
        "core/_post_items.html",
        {"posts": page_obj.object_list, "query": query}
    )

    return JsonResponse({
        "html": html,
        "has_next": page_obj.has_next(),
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
    })

