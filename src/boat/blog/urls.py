from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('blog/post_list', views.PostList.as_view(), name='post-list'),
    path('blog/post_create', views.postCreate, name='post-create'),
    path('blog/post_detail/<int:pk>', views.PostDetail.as_view(), name='post-detail'),
    path('blog/post_delete/<int:pk>', views.PostDelete.as_view(), name='post-delete'),
    path('blog/post_update/<int:pk>', views.PostUpdate.as_view(), name='post-update'),
    path('blog/post_veroeffentlichen/<int:pk>', views.postPublish, name='post-publish'),
]
