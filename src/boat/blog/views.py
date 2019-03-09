from django.shortcuts import render
from django.utils import timezone
from django.generic import TemplateView, ListView, DetailView
from django.view.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from .models import Post


# Create your views here.
class PostList(LoginRequiredMixin, ListView)
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    model = Post
    paginate_by = 10
    queryset = models.Blog.objects.order_by('published_date')
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
