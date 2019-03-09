from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('blog/post_list', views.post_list, name='post-list'),
]
