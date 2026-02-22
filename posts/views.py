from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import PostImage, Post
from django.contrib import messages


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        images = request.FILES.getlist("images")

        if form.is_valid():
            if not images:
                form.add_error(None, "Нужно загрузить хотя бы 1 фото")
            elif len(images) > 5:
                form.add_error(None, "Можно загрузить максимум 5 фото")
            else:
                post = form.save(commit=False)
                post.author = request.user
                post.save()

                for image in images:
                    PostImage.objects.create(post=post, image=image)

                return redirect("core:home")
    else:
        form = PostForm()

    return render(request, "posts/create_post.html", {"form": form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/post_detail.html", {"post": post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("core:home")

    if request.method == "POST":
        post.delete()
        messages.success(request, "Пост удалён")
        return redirect("users:profile")

    return redirect("posts:post_detail", pk=pk)


