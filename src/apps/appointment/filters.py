import django_filters
from django import forms
from apps.appointment.models import Availability

class AvailabilityFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFilter
    class Meta:
        model = Availability
        fields = ('')