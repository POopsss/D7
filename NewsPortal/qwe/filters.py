from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter, Filter
from .models import Post, Category
from django.forms import DateTimeInput


class NewsFilter(FilterSet):
    title = Filter(
        field_name='title',
        lookup_expr='icontains',
        label='Поиск в названии статьи',
    )

    category = ModelMultipleChoiceFilter(
        field_name='postcategory__categoryThrough',
        queryset=Category.objects.all(),
        label='Категории',
        conjoined=True,
    )

    added_after = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Опубликовано после',
    )