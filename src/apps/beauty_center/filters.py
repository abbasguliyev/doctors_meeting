import django_filters
from django import forms
from django.db.models import Q, Value
from django.db.models.functions import Concat
from apps.beauty_center import models

class BeautyCenterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={
        'class': 'search-hospital',
        'name': 'name'
    }), required=False)
    country = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={
        'class': 'search-hospital',
        'name': 'country'
    }), required=False)
    city = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={
        'class': 'search-hospital',
        'name': 'city'
    }), required=False)
    address = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={
        'class': 'search-hospital',
        'name': 'address'
    }), required=False)

    class Meta:
        model = models.BeautyCenter
        fields = {
            'name', 'country', 'city', 'address'
        }