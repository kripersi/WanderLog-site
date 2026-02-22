from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
]
