from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscription
from .filters import NewsFilter
from .forms import PostForm

from django.http import HttpResponse
from django.views import View


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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('qwe.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


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


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('qwe.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('qwe.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(Subscription.objects.filter(user=request.user, category=OuterRef('pk')))
    ).order_by('category')
    return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions})

# from django.http import HttpResponse
# from django.views import View
# from .tasks import task
#
# class IndexView(View):
#     def get(self, request):
#         task.delay()
#         return HttpResponse('Hello!')