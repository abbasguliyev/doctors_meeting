from typing import Any
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q, Value
from django.http import HttpRequest, HttpResponse, JsonResponse

from django.db.models.functions import Concat
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site

from django.core.paginator import Paginator


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from doctors_meeting.utils import generate_random_slug
from apps.authentication import enums, selectors, tasks, filters
from apps.authentication.forms import (
    RegisterDoctorForm, 
    RegisterUserForm, 
    LoginForm, 
    UpdateUserForm, 
    UpdateDoctorUserForm,
    UpdatePatientUserForm,
    ExperienceForm,
    EducationForm,
    ChangePasswordForm,
    UserSocialMediaForm,
    PatientFileForm
)
from apps.authentication.models import DoctorProfile, PatientProfile, Experience, Education, UserSocialMedia, PatientsFile
from apps.authentication.tokens import account_activation_token
from apps.authentication.utils import do_offline, do_online

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('index')


class RegisterDoctorView(CreateView):
    form_class = RegisterDoctorForm
    success_url = reverse_lazy('index')
    template_name = 'doctor-register.html'

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            messages.info(request, "Please logout for be a doctor!")
            return redirect(reverse_lazy('index'))
        return render(request, self.template_name, context={'form': form})
    
    def form_valid(self, form):
        user = form.save(commit=False)
        email = form.cleaned_data.get('email')
        user.user_type = enums.UserType.doctor
        user.is_active = False
        user.save()
        if selectors.doctor_profile_list().filter(user=user).count() == 0:
            user_doctor_profile = DoctorProfile.objects.create(user=user)
            slug = generate_random_slug(name=f"{user.first_name} {user.last_name}", query_list=selectors.doctor_profile_list())
            user_doctor_profile.slug = slug
            user_doctor_profile.save()
        transaction.on_commit(lambda: tasks.send_activication_email_task.delay(get_current_site(self.request).domain, self.request.is_secure(), user.id, email))
        messages.success(self.request, "Please check your mail address")

        return super().form_valid(form)

class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect(reverse_lazy('index'))
        return render(request, self.template_name, context={'form': form})
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = enums.UserType.patient
        user.save()
        if selectors.patient_profile_list().filter(user=user).count() == 0:
            user_patient_profile = PatientProfile.objects.create(user=user)
            user_patient_profile.save()
        messages.success(self.request, "You have successfully registered")
        return super().form_valid(form)

class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect(reverse_lazy('index'))
        return render(request, self.template_name, context={'form': form})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password'),
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    do_online(user)
                    messages.success(request, f'Welcome {user.first_name} {user.last_name}')
                    return redirect(reverse_lazy('index'))
                else:
                    messages.error(request, 'Disabled Account')
            else:
                messages.error(request, 'Check Your Username and Password')

        return render(request, self.template_name, context={'form': form})

class LogoutView(LoginRequiredMixin, View):
    """
    This view is for the logout process
    """

    def get(self, request):
        do_offline(request.user)
        logout(request)
        return redirect(reverse_lazy('login'))
    
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, check your email"
    success_url = reverse_lazy('login')
    
class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "profile.html"
    context_object_name = "user"

    def get(self, request: HttpRequest, pk, *args: Any, **kwargs: Any) -> HttpResponse:
        search_user = selectors.user_list().filter(pk=pk).last()
        if search_user != request.user:
            return redirect('profile', pk=request.user.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor_profile'] = selectors.doctor_profile_list().filter(user=self.request.user).last()
        context['patient_profile'] = selectors.patient_profile_list().filter(user=self.request.user).last()
        return context
    
class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy("index")
    template_name = "change_password.html"

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Password Changed')
        return super().form_valid(form)

    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UpdateUserForm
    template_name = 'user_profile.html'
    context_object_name = "user"

    def get(self, request: HttpRequest, pk, *args: Any, **kwargs: Any) -> HttpResponse:
        search_user = selectors.user_list().filter(pk=pk).last()
        if search_user != request.user:
            return redirect('profile_update', pk=request.user.pk)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        if self.request.user.user_type == enums.UserType.doctor:
            form_class = UpdateDoctorUserForm
        elif self.request.user.user_type == enums.UserType.patient:
            form_class = UpdatePatientUserForm
        else:
            form_class = self.form_class
        self.form_class = form_class
        return self.form_class
    
    def get_initial(self):
        initial = super().get_initial()
        if self.form_class == UpdateDoctorUserForm:
            profile = selectors.doctor_profile_list().filter(user=self.request.user).last()
            initial["currency_unit"] = profile.currency_unit
            initial["about_doctor"] = profile.about_doctor
            initial["avatar"] = profile.avatar
            initial["country"] = profile.country
            initial["city"] = profile.city
            initial["profession"] = profile.profession
            initial["title"] = profile.title
            initial["orcid_account"] = profile.orcid_account
            initial["pubmed_account"] = profile.pubmed_account
            initial["diseases"] = profile.diseases.all()
        return initial

    def form_valid(self, form):
        if self.form_class == UpdateDoctorUserForm:
            profile_data = dict()
            currency_unit = form.cleaned_data.pop('currency_unit')
            about_doctor = form.cleaned_data.pop('about_doctor')
            avatar = form.cleaned_data.pop('avatar')
            country = form.cleaned_data.pop('country')
            city = form.cleaned_data.pop('city')
            profession = form.cleaned_data.pop('profession')
            title = form.cleaned_data.pop('title')
            orcid_account = form.cleaned_data.pop('orcid_account')
            pubmed_account = form.cleaned_data.pop('pubmed_account')
            diseases = form.cleaned_data.pop('diseases')

            profile_data["currency_unit"] = currency_unit
            profile_data["about_doctor"] = about_doctor
            if avatar == None:
                profile_data["avatar"] = selectors.doctor_profile_list().filter(user=self.request.user).last().avatar
            else:
                profile_data["avatar"] = avatar
            profile_data["country"] = country
            profile_data["city"] = city
            profile_data["profession"] = profession
            profile_data["title"] = title
            profile_data["orcid_account"] = orcid_account
            profile_data["pubmed_account"] = pubmed_account
            
            user_doctor_profile = selectors.doctor_profile_list().filter(user=self.request.user).update(**profile_data)
            user_doctor_profile = selectors.doctor_profile_list().filter(user=self.request.user).last()
            user_doctor_profile.avatar = avatar
            user_doctor_profile.city = city
            user_doctor_profile.diseases.set(diseases)
            slug = generate_random_slug(name=f"{self.request.user.first_name} {self.request.user.last_name}", query_list=selectors.doctor_profile_list())
            user_doctor_profile.slug = slug
            user_doctor_profile.save()

        messages.success(self.request, 'Profile successfully edited!')
        return super().form_valid(form)
    
class ExperienceCreateView(LoginRequiredMixin, CreateView):
    form_class = ExperienceForm
    success_url = reverse_lazy('experience')
    template_name = 'experience_create.html'
    context_object_name = 'experiences'

    def form_valid(self, form):
        doctor_profile = selectors.doctor_profile_list().filter(user=self.request.user).last()
        if doctor_profile is None:
            messages.error(self.request, "You are not a doctor")
            return redirect(reverse_lazy('index'))
        experience = form.save(commit=False)
        experience.user = doctor_profile
        experience.save()
        messages.success(self.request, "Experience added successfully")
        return super().form_valid(form)
    
class ExperienceListView(LoginRequiredMixin, ListView):
    model = Experience
    paginate_by = 4
    template_name = "experience.html"
    context_object_name = "experiences"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_profile = selectors.doctor_profile_list().filter(user=self.request.user).last()
        experiences = selectors.experience_list().filter(user=doctor_profile)
        if experiences.count() == 0:
            context['experiences'] = None
        else:
            context['experiences'] = experiences
        return context
    
class ExperienceDetailView(LoginRequiredMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'experience_detail.html'
    success_url = reverse_lazy('experience')
    context_object_name = "experience"

class ExperienceDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        experience = selectors.experience_list().filter(pk=pk).last()
        if experience is not None:
            experience.delete()
        messages.success(request, "Successfully deleted!")
        return redirect("experience")


class EducationCreateView(LoginRequiredMixin, CreateView):
    form_class = EducationForm
    success_url = reverse_lazy('education')
    template_name = 'education_create.html'
    context_object_name = 'educations'

    def form_valid(self, form):
        doctor_profile = selectors.doctor_profile_list().filter(user=self.request.user).last()
        if doctor_profile is None:
            messages.error(self.request, "You are not a doctor")
            return redirect(reverse_lazy('index'))
        education = form.save(commit=False)
        education.user = doctor_profile
        education.save()
        messages.success(self.request, "Education added successfully")
        return super().form_valid(form)
    
class EducationListView(LoginRequiredMixin, ListView):
    model = Education
    paginate_by = 4
    template_name = "education.html"
    context_object_name = "educations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_profile = selectors.doctor_profile_list().filter(user=self.request.user).last()
        educations = selectors.education_list().filter(user=doctor_profile)
        if educations.count() == 0:
            context['educations'] = None
        else:
            context['educations'] = educations
        return context
    
class EducationDetailView(LoginRequiredMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'education_detail.html'
    success_url = reverse_lazy('education')
    context_object_name = "education"

class EducationDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        education = selectors.education_list().filter(pk=pk).last()
        if education is not None:
            education.delete()
        messages.success(request, "Successfully deleted!")
        return redirect("education")
    
class DoctorListView(ListView):
    model = DoctorProfile
    paginate_by = 10
    queryset = selectors.doctor_profile_list().filter(status=enums.DoctorAcceptedStatus.accepted, hospital=None, beauty_center=None)
    template_name = "doctors.html"
    context_object_name = "doctors"

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = filters.DoctorFilter(self.request.GET, queryset=queryset).qs
        return filtered_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["professions"] = selectors.profession_list()
        
        # Filter the result
        filter = filters.DoctorFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter
        queryset = filter.qs

        # Paginate the results
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
    
class DoctorDetailView(DetailView):
    model = DoctorProfile
    template_name = "doctor_detail.html"
    context_object_name = 'doctor'

    def get(self, request, *args, **kwargs):
        doctor = self.get_object()
        if doctor.status != "Accepted":
            return redirect('doctors')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        user = instance.user
        context['experiences'] = selectors.experience_list().filter(user=instance)
        context['educations'] = selectors.education_list().filter(user=instance)
        context['diseases'] = instance.diseases.all()
        context['social_medias'] = UserSocialMedia.objects.select_related('user').filter(user=instance)
        print(f"{context['diseases']=}")
        return context
    
def load_cities(request):
    country_id = request.GET.get('country')
    try:
        cities = selectors.city_list().filter(country=country_id)
    except:
        cities = []
    city_list = []
    for city in cities:
        city_list.append({'id': city.id, 'name': city.name})
    
    try:
        current_city = request.user.doctor_profile.city
        current_city_json = {'id': current_city.id, 'name': current_city.name}
        return JsonResponse({'cities': city_list, 'current_city': current_city_json})
    except:
        current_city_json = {'id': 0, 'name': ''}
        return JsonResponse({'cities': city_list, 'current_city': current_city_json})

class UserSocialMediaListView(ListView):
    model = UserSocialMedia
    paginate_by = 10
    template_name = "user_social_media.html"
    context_object_name = "user_social_medias"

    def get_queryset(self):
        # user = selectors.user_list().filter(pk=self.request.user.pk).last()
        doctor_profile = selectors.doctor_profile_list().filter(user=self.request.user).last()
        return super().get_queryset().filter(user=doctor_profile)
    
class UserSocialMediaCreateView(LoginRequiredMixin, CreateView):
    form_class = UserSocialMediaForm
    success_url = reverse_lazy('social_media')
    template_name = 'user_social_media_create.html'
    context_object_name = 'user_social_medias'

    def form_valid(self, form):
        doctor_profile = selectors.doctor_profile_list().filter(user=self.request.user).last()
        if doctor_profile is None:
            messages.error(self.request, "You are not a doctor")
            return redirect(reverse_lazy('index'))
        social_media = form.save(commit=False)
        social_media.user = doctor_profile
        social_media.save()
        messages.success(self.request, "Social media added successfully")
        return super().form_valid(form)
    
class UserSocialMediaDetailView(LoginRequiredMixin, UpdateView):
    model = UserSocialMedia
    form_class = UserSocialMediaForm
    template_name = 'user_social_media_detail.html'
    success_url = reverse_lazy('social_media')
    context_object_name = "user_social_medias"

class UserSocialMediaDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        social_media = UserSocialMedia.objects.select_related('user').filter(pk=pk).last()
        if social_media is not None:
            social_media.delete()
        messages.success(request, "Successfully deleted!")
        return redirect("social_media")
    
class PatientFileListView(ListView):
    model = PatientsFile
    paginate_by = 10
    template_name = "patient_file.html"
    context_object_name = "patient_files"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_profile = selectors.patient_profile_list().filter(user=self.request.user).last()
        patient_files = selectors.patient_file_list().filter(patient=patient_profile)
        if patient_files.count() == 0:
            context['patient_files'] = None
        else:
            context['patient_files'] = patient_files
        return context

class PatientFileCreateView(LoginRequiredMixin, CreateView):
    form_class = PatientFileForm
    success_url = reverse_lazy('patient_files')
    template_name = 'patient_file_create.html'
    context_object_name = 'patient_files'

    def form_valid(self, form):
        patient_profile = selectors.patient_profile_list().filter(user=self.request.user).last()
        if patient_profile is None:
            messages.error(self.request, "You are not a patient")
            return redirect(reverse_lazy('index'))
        patient_file = form.save(commit=False)
        patient_file.patient = patient_profile
        patient_file.save()
        messages.success(self.request, "File added successfully")
        return super().form_valid(form)
    
class PatientFileDetailView(LoginRequiredMixin, UpdateView):
    model = PatientsFile
    form_class = PatientFileForm
    template_name = 'patient_file_detail.html'
    success_url = reverse_lazy('patient_files')
    context_object_name = "patient_files"

class PatientFileDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        patient_file = selectors.patient_file_list().filter(pk=pk).last()
        if patient_file is not None:
            patient_file.delete()
        messages.success(request, "Successfully deleted!")
        return redirect("patient_files")