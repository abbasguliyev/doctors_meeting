from typing import Any, Dict
from django.shortcuts import render
from django.db.models import Q, Value
from django.db.models.functions import Concat

from django.core.paginator import Paginator

from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from apps.beauty_center.models import BeautyCenter
from apps.beauty_center import filters
from apps.authentication import selectors as auth_selectors, enums, filters as auth_filter

class BeautyCenterListView(ListView):
    model = BeautyCenter
    paginate_by = 10
    template_name = "beauty_center.html"
    context_object_name = "beauty_centers"

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = filters.BeautyCenterFilter(self.request.GET, queryset=queryset).qs
        return filtered_queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter the result
        filter = filters.BeautyCenterFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter
        queryset = filter.qs

        # Paginate the results
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

    
class BeautyCenterDoctorListView(DetailView):
    model = BeautyCenter
    paginate_by = 10
    template_name = "beauty_center_doctors.html"
    context_object_name = 'beauty_center'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter the result
        doctor_qs = auth_selectors.doctor_profile_list().filter(beauty_center__pk=self.get_object().pk)
        filter = auth_filter.DoctorFilter(self.request.GET, queryset=doctor_qs)
        context['filter'] = filter
        doctor_queryset = filter.qs
        context['doctor_count'] = doctor_queryset.count()

        # Paginate the results
        paginator = Paginator(doctor_queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['doctors'] = page_obj
        return context