from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('blog/post_list', views.PostList.as_view(), name='post-list'),
    path('blog/post_create', views.postCreate, name='post-create'),
]