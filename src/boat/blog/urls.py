from django.urls import path
from . import views

urlpatterns = [
    path('blog/post_list', name='post-list'),
]
