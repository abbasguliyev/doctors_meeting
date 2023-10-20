from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from doctors_meeting.utils import generate_random_slug

from apps.blog.forms import BlogForm
from apps.blog.models import Blog
from apps.blog.selectors import blog_list
from apps.authentication.selectors import doctor_profile_list

class BlogView(ListView):
    model = Blog
    paginate_by = 4
    template_name = "blog.html"
    context_object_name = "blogs"

    def get_queryset(self) -> QuerySet[Any]:
        title = self.request.GET.get('title')
        if title is not None:
            return super().get_queryset().filter(title__icontains=title)
        else:
            return super().get_queryset()
        
class DoctorBlogView(ListView):
    model = Blog
    paginate_by = 4
    template_name = "doctor_blog.html"
    context_object_name = "blogs"

    def get_queryset(self) -> QuerySet[Any]:
        pk = self.kwargs.get('pk')
        title = self.request.GET.get('title')
        if title is not None:
            doctor_profile = doctor_profile_list().filter(pk=pk).last()
            return super().get_queryset().filter(author=doctor_profile, title__icontains=title)
        else:
            doctor_profile = doctor_profile_list().filter(pk=pk).last()
            return super().get_queryset().filter(author=doctor_profile)
        
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['doctor'] = doctor_profile_list().filter(pk=pk).last()
        return context
class BlogDetailView(DetailView):
    model = Blog
    paginate_by = 10
    template_name = "blog_detail.html"
    context_object_name = 'blog'

class ProfileBlogView(ListView):
    model = Blog
    paginate_by = 4
    template_name = "profile_blog.html"
    context_object_name = "blogs"

    def get_queryset(self) -> QuerySet[Any]:
        doctor_profile = doctor_profile_list().filter(user=self.request.user).last()
        return super().get_queryset().filter(author=doctor_profile)

class ProfileBlogCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    success_url = reverse_lazy('profile_blog')
    template_name = 'profile_blog_create.html'

    def form_valid(self, form):
        doctor_profile = doctor_profile_list().filter(user=self.request.user)
        if doctor_profile is None:
            messages.error(self.request, "You are not a doctor")
            return redirect('profile_blog')
        blog = form.save(commit=False)
        blog.author = doctor_profile.last()
        slug = generate_random_slug(name=f"{blog.title}", query_list=blog_list())
        blog.slug = slug
        blog.save()
        messages.success(self.request, "Blog added successfully")
        return super().form_valid(form)

class ProfileBlogDetailView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'profile_blog_update.html'
    context_object_name = "blog"

    def get_success_url(self):
        return reverse('profile_blog')
    
class ProfileBlogDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        blog = blog_list().filter(slug=slug).last()
        if blog is not None:
            blog.delete()
        messages.success(request, "Successfully deleted!")
        return redirect("profile_blog")