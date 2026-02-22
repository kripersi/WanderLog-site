from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from posts.models import Post

from .forms import UserRegisterForm, ProfileUpdateForm


def users_home(request):
    return render(request, 'users/users.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Аккаунт создан!")
            login(request, user)
            return redirect('core:home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, username=None):
    # Если username передан то смотрим чужой профиль
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user

    posts = Post.objects.filter(author=user_obj).order_by('-created_at')

    is_owner = request.user == user_obj

    form = None

    if is_owner:
        profile_instance = user_obj.profile

        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)
            if form.is_valid():
                form.save()
                return redirect('users:profile')
        else:
            form = ProfileUpdateForm(instance=profile_instance)

    return render(request, 'users/profile.html', {
        'profile_user': user_obj,
        'posts': posts,
        'form': form,
        'is_owner': is_owner
    })


def logout_user(request):
    logout(request)
    return redirect('core:home')


@login_required
def likes(request):
    liked_posts = (
        Post.objects.filter(likes__user=request.user)
        .select_related("author")
        .prefetch_related("images")
        .order_by("-likes__created_at")
    )
    return render(request, "users/likes.html", {"liked_posts": liked_posts})

