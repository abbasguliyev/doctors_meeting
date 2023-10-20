from typing import Any, Dict
import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View

from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation

from django.db.models import Q, Value
from django.db.models.functions import Concat

from django.core.paginator import Paginator
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from apps.authentication.models import DoctorProfile
from apps.authentication import selectors as auth_selectors, enums
from apps.pages.forms import AdsCommentForm
from apps.pages.models import Contact, Ads, AdsComment, AdsReport, AdsClick, News, Conference
from apps.blog.models import Blog
from apps.hospital.models import Hospital
from apps.beauty_center.models import BeautyCenter

class IndexView(ListView):
    model = DoctorProfile
    paginate_by = 3
    template_name = "index.html"
    context_object_name = "doctors"
    queryset = auth_selectors.doctor_profile_list().filter(status=enums.DoctorAcceptedStatus.accepted)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ads = Ads.objects.filter(is_active = True).order_by('-pk')
        news = News.objects.all().order_by('-pk')[:3]
        confs = Conference.objects.all().order_by('-pk')[:3]
        blogs = Blog.objects.select_related('author').all().order_by('-pk')[:3]
        context['ads'] = ads
        context['news'] = news
        context['confs'] = confs
        context['blogs'] = blogs
        return context
    
class AdsView(DetailView):
    model = Ads
    template_name = "ads.html"
    context_object_name = "ads" 

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        comments = AdsComment.objects.filter(ads=self.get_object()).order_by('-pk')
        context['comments'] = comments
        context['form'] = AdsCommentForm
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated == True:
            login_user = request.user
            print(f"{login_user=}")
            user_ads_click_count = AdsClick.objects.select_related('ads', 'user').filter(ads=self.get_object(), user=login_user, click_date=datetime.date.today()).count()
            if user_ads_click_count == 0:
                AdsClick.objects.create(ads=self.get_object(), user=login_user, click_date=datetime.date.today())
                ads_report = AdsReport.objects.select_related('ads').filter(ads=self.get_object(), report_date = datetime.date.today()).last()
                if ads_report is None:
                    ads_report = AdsReport.objects.create(ads=self.get_object(), report_date = datetime.date.today())
                    if request.user.gender == enums.GenderOptions.MALE:
                        ads_report.man_count = ads_report.man_count + 1
                    elif request.user.gender == enums.GenderOptions.FEMALE:
                        ads_report.women_count = ads_report.women_count + 1
                    ads_report.total_count = ads_report.total_count + 1
                    ads_report.save()
                else:
                    if request.user.gender == enums.GenderOptions.MALE:
                        ads_report.man_count = ads_report.man_count + 1
                    elif request.user.gender == enums.GenderOptions.FEMALE:
                        ads_report.women_count = ads_report.women_count + 1
                    ads_report.total_count = ads_report.total_count + 1
                    ads_report.save()
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('login'))

class AdsCommentView(LoginRequiredMixin, CreateView):
    model = AdsComment
    form_class = AdsCommentForm
    template_name = "ads.html"

    def form_valid(self, form):
        ads_comment = form.save(commit=False)
        owner = self.request.user
        ads = form.cleaned_data.get("ads")
        comment = form.cleaned_data.get('comment')
        ads_comment.owner = owner
        ads_comment.ads = ads
        ads_comment.comment = comment
        ads_comment.save()
        messages.success(self.request, "Thanks for your comment")
        return redirect("ad_detail", slug=ads.slug)

class IndexDoctorPaginationView(ListView):
    model = DoctorProfile
    paginate_by = 3
    template_name = "doctor_index_pagination.html"
    context_object_name = "doctors"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctors_a = auth_selectors.doctor_profile_list().filter(status=enums.DoctorAcceptedStatus.accepted)
        paginator = Paginator(doctors_a, self.paginate_by)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        doctors = paginator.page(page)
        context["doctors"] = doctors
        context["page_obj"] = page_obj
        return context

class IndexDoctorSearchView(View):
    def get(self, request):
        q = request.GET.get('q')
        print(f"{q=}")
        dynamic_url = reverse_lazy('index')
        doctors = auth_selectors.doctor_profile_list().filter(status=enums.DoctorAcceptedStatus.accepted).annotate(full_name=Concat('user__first_name', Value(" "), 'user__last_name')).filter(Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(full_name__icontains=q)).count()
        if doctors > 0:
            dynamic_url = reverse_lazy('doctors') + f"?fullname={q}"
        else:
            messages.info(request, 'No result found')
        return redirect(dynamic_url)
    
class IndexFacilitySearchView(View):
    def get(self, request):
        q = request.GET.get('q')
        facility = request.GET.get('facility')
        print(f"{q=}")
        print(f"{facility=}")
        dynamic_url = reverse_lazy('index')
        hospitals = Hospital.objects.filter(name__icontains=q).count()
        beauty_centers =  BeautyCenter.objects.filter(name__icontains=q).count()
        if facility == "hospital":
            if hospitals > 0:
                dynamic_url = reverse_lazy('hospitals') + f"?name={q}"
            else:
                messages.info(request, 'No result found')
        elif facility == "beauty_center":
            if beauty_centers > 0:
                dynamic_url = reverse_lazy('beauty_centers') + f"?name={q}"
            else:
                messages.info(request, 'No result found')
        return redirect(dynamic_url)
    
class IndexIssueSearchView(View):
    def get(self, request):
        q = request.GET.get('q')
        print(f"{q=}")
        dynamic_url = reverse_lazy('index')
        doctors = auth_selectors.doctor_profile_list().filter(diseases__name__icontains=q).count()
        if doctors > 0:
            dynamic_url = reverse_lazy('doctors') + f"?diseases={q}"
        else:
            messages.info(request, 'No result found')
        return redirect(dynamic_url)

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(View):
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact.objects.create(name=name, email=email, subject=subject, phone=phone, message=message)
        contact.full_clean()
        contact.save()
        messages.success(request, "Message successfully sended")
        return redirect('index')
    
class IndexNewsPaginationView(ListView):
    model = News
    paginate_by = 3
    template_name = "news_index_pagination.html"
    context_object_name = "news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = News.objects.all()
        paginator = Paginator(news, self.paginate_by)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        news = paginator.page(page)
        context["page_obj"] = page_obj
        return context
    
class IndexConfPaginationView(ListView):
    model = Conference
    paginate_by = 3
    template_name = "conf_index_pagination.html"
    context_object_name = "confs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        confs = Conference.objects.all()
        paginator = Paginator(confs, self.paginate_by)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        confs = paginator.page(page)
        context["page_obj"] = page_obj
        return context
    
class IndexBlogPaginationView(ListView):
    model = Blog
    paginate_by = 3
    template_name = "blog_index_pagination.html"
    context_object_name = "blogs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.select_related('author').all()
        paginator = Paginator(blogs, self.paginate_by)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        blogs = paginator.page(page)
        context["page_obj"] = page_obj
        return context
    
class NewsListView(ListView):
    model = News
    paginate_by = 4
    template_name = "news.html"
    context_object_name = "news"

    def get_queryset(self):
        title = self.request.GET.get('title')
        if title is not None:
            return super().get_queryset().filter(title__icontains=title)
        else:
            return super().get_queryset()
        
class NewsDetailView(DetailView):
    model = News
    paginate_by = 10
    template_name = "news_detail.html"
    context_object_name = 'new'

class ConferenceListView(ListView):
    model = Conference
    paginate_by = 4
    template_name = "conference.html"
    context_object_name = "conferences"

    def get_queryset(self):
        title = self.request.GET.get('title')
        if title is not None:
            return super().get_queryset().filter(title__icontains=title)
        else:
            return super().get_queryset()
        
class ConferenceDetailView(DetailView):
    model = Conference
    paginate_by = 10
    template_name = "conference_detail.html"
    context_object_name = 'conference'


def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response