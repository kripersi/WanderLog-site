from django.urls import path
from .views import home, feed

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('feed/', feed, name='feed'),
]
