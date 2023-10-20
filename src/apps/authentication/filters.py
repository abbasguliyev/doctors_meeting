import django_filters
from django import forms
from apps.authentication import enums, selectors, models
from django.db.models import Q, Value
from django.db.models.functions import Concat

class DoctorFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(method='filter_fullname', widget=forms.TextInput(attrs={
        'class': 'search-doctor',
        'name': 'fullname'
    }), required=False)
    profession = django_filters.ModelChoiceFilter(queryset = selectors.profession_list(), widget=forms.Select(attrs={
        'class': 'doctor-search-form-select',
        'placeholder': 'Profession',
        'name': 'profession'
    }), required=False)
    country = django_filters.CharFilter(method='filter_country', widget=forms.TextInput(attrs={
        'class': 'search-doctor',
        'name': 'country'
    }), required=False)
    city = django_filters.CharFilter(method='filter_city', widget=forms.TextInput(attrs={
        'class': 'search-doctor',
        'name': 'city'
    }), required=False)
    diseases = django_filters.ModelChoiceFilter(queryset = selectors.disease_list(), widget=forms.Select(attrs={
        'class': 'doctor-search-form-select',
        'placeholder': 'Disease',
        'name': 'disease'
    }), required=False)

    class Meta:
        model = models.DoctorProfile
        fields = {
            'profession', 'diseases'
        }

    def filter_fullname(self, queryset, name, value):
        queryset = queryset.annotate(full_name=Concat('user__first_name', Value(" "), 'user__last_name'))
        return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(full_name__icontains=value))
    
    def filter_country(self, queryset, name, value):
        return queryset.filter(Q(country__name__icontains=value))
    
    def filter_city(self, queryset, name, value):
        return queryset.filter(Q(city__name__icontains=value))