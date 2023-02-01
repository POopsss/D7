from django.contrib import admin
from django.urls import path, include

from django.urls import path
from .views import *



urlpatterns = [
   path('news/', NewsList.as_view(), name='news_list'),
   path('article/', ArticleList.as_view(), name='article_list'),
   path('post/<pk>', PostDetail.as_view(), name='post_detail'),
   path('news/<pk>', NewsDetail.as_view(), name='news_detail'),
   path('article/<pk>', ArticleDetail.as_view(), name='article_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('news/<pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('article/<pk>/edit/', PostUpdate.as_view(), name='article_update'),
   path('news/<pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('article/<pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]