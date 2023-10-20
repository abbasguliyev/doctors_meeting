import django_filters
from django import forms
from django.db.models import Q, Value
from django.db.models.functions import Concat
from apps.blog.models import Blog

class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={
        'class': 'search-hospital',
        'name': 'name'
    }), required=False)

    class Meta:
        model = Blog
        fields = {'title'}