from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.contrib.auth.decorators import login_required
from .models import Post
from . import forms

# Create your views here.
class PostList(LoginRequiredMixin, ListView):
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    model = Post
    paginate_by = 10
    queryset = models.Blog.objects.order_by('published_date')
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'

@login_required(login_url='account:login')
def postCreate(request):
    author = request.user
    if request.method == 'POST':
        form = forms.PostCreateForm(data=request.POST)
        if form.is_valid():
            if request.POST.__contains__('Speichern'):
                post = Post()
                post.author = author
                post.text = form.cleaned_data.get('text')
                post.created_date = datetime.datetime.now()
                post.title = form.cleaned_data.get('title')
                post.save()
                return HttpResponseRedirect(reverse('blog:post-list'))
            if request.POST.__contains__('Veröffentlichen'):
                post = Post()
                post.author = author
                post.text = form.cleaned_data.get('text')
                post.created_date = datetime.datetime.now()
                post.published_date = datetime.datetime.now()
                post.title = form.cleaned_data.get('title')
                post.save()
                return HttpResponseRedirect(reverse('blog:post-list'))
    else:
        form = forms.PostCreateForm()
        return render(request,'blog/post_create.html',{'form':form})