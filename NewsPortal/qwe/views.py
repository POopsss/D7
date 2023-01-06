from django.views.generic import ListView, DetailView
from .models import *


class NewsList(ListView):
    model = Post
    ordering = '-date'
    # queryset = Product.objects.filter(price__lt=100).order_by('-name')
    template_name = 'news.html'

    context_object_name = 'news'


class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
