import django_filters
from django import forms
from apps.authentication import enums, selectors, models
from django.db.models import Q, Value
from django.db.models.functions import Concat

class DashboardUserFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(method='filter_fullname', widget=forms.TextInput(attrs={
        'class': 'custom-admin-user-input',
        'name': 'fullname',
        'placeholder': 'Fullname'
    }), required=False)
    user_type = django_filters.ChoiceFilter(choices=enums.UserType.choices,  widget=forms.Select(attrs={
        'class': 'custom-admin-user-input'
    }))

    class Meta:
        model = models.User
        fields = {
            'user_type'
        }

    def filter_fullname(self, queryset, name, value):
        queryset = queryset.annotate(full_name=Concat('first_name', Value(" "), 'last_name'))
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(full_name__icontains=value))