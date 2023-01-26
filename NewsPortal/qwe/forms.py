from django import forms
from django.core.exceptions import ValidationError
from django_filters import ModelMultipleChoiceFilter

from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    postAuthor = forms.ModelChoiceField(queryset=Author.objects.all(), label='Автор')
    title = forms.CharField(min_length=4, label='Заголовок')
    text = forms.CharField(widget=forms.Textarea, min_length=4, label='Содержание')
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Категории')

    class Meta:
        model = Post
        fields = ['postAuthor', 'title', 'text', 'category']

    # Немного мусора
    # def clean(self):
    #     cleaned_data = super().clean()
    #     description = cleaned_data.get("description")
    #     name = cleaned_data.get("name")
    #
    #     if name == description:
    #         raise ValidationError(
    #             "Описание не должно быть идентично названию."
    #         )
    #
    #     return cleaned_data