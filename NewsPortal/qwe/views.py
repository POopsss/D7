from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import NewsFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsList(PostList):
    queryset = Post.objects.filter(postType='NE')


class ArticleList(PostList):
    queryset = Post.objects.filter(postType='AR')


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewsDetail(PostDetail):
    queryset = Post.objects.filter(postType='NE')


class ArticleDetail(PostDetail):
    queryset = Post.objects.filter(postType='AR')


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsCreate(PostCreate):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.postType = 'NE'
        return super().form_valid(form)


class ArticleCreate(PostCreate):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.postType = 'AR'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
