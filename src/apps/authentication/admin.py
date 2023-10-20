from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from doctors_meeting.utils import generate_random_slug
from apps.authentication import models, enums, selectors
from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)
from django_celery_results.models import TaskResult, GroupResult
from cities_light.models import Region, SubRegion

admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
admin.site.unregister(Region)
admin.site.unregister(SubRegion)


class ExperienceInline(admin.TabularInline):
    model = models.Experience
    extra = 0

class EducationInline(admin.TabularInline):
    model = models.Education
    extra = 0

class UserSocialMediaInline(admin.TabularInline):
    model = models.UserSocialMedia
    extra = 0

class PatientsFileInline(admin.TabularInline):
    model = models.PatientsFile
    extra = 0

class UserAdmin(BaseUserAdmin):
    model = get_user_model()
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'gender', 'birth_date', 'is_superuser', 
            'is_staff', 'groups', 'user_permissions', 'is_active',
            'date_joined', 'last_login', 'user_type', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'gender', 'birth_date', 'is_superuser', 
            'is_staff', 'groups', 'user_permissions', 'is_active',
            'date_joined', 'last_login', 'user_type', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'gender', 'birth_date', 'user_type', 'is_online')
    list_display_links = ('id', 'email')
    list_filter = ('user_type', 'email', 'first_name', 'last_name', 'gender', 'birth_date')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id',)

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        user_type = form.cleaned_data.get('user_type')
        super().save_model(request, obj, form, change)
        if user_type == enums.UserType.doctor:
            if selectors.doctor_profile_list().filter(user=obj).count() == 0:
                user_doctor_profile = models.DoctorProfile.objects.create(user=obj)
                slug = generate_random_slug(name=f"{obj.first_name} {obj.last_name}", query_list=selectors.doctor_profile_list())
                user_doctor_profile.slug = slug
                user_doctor_profile.save()
        else:
            if selectors.patient_profile_list().filter(user=obj).count() == 0:
                user_patient_profile = models.PatientProfile.objects.create(user=obj)
                user_patient_profile.save()

admin.site.register(get_user_model(), UserAdmin)

@admin.register(models.Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'experience_place', 'city', 'start_year', 'end_year')

@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'education_place', 'education_branch', 'city', 'start_year', 'end_year')

@admin.register(models.DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    inlines = [ExperienceInline, EducationInline, UserSocialMediaInline]
    filter_horizontal = ['diseases']
    list_display = ('id', 'user', 'profession', 'title', 'status')
    list_filter = ('title', 'status', 'profession')
    list_display_links = ('id', 'user')
    
    readonly_fields = ('id_card',)

    def id_card(self, obj):
        from django.utils.html import format_html
        return format_html("<a href='%s'>%s</a>" % (obj.user.id_card.url, obj.user.id_card.url))
    
    id_card.allow_tags = True


@admin.register(models.PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    inlines = [PatientsFileInline]

    list_display = ('id', 'user')
    list_display_links = ('id', 'user')

@admin.register(models.PatientsFile)
class PatientFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'patient')
    list_display_links = ('id', 'name', 'patient')
    list_filter = ('name', 'patient')

@admin.register(models.Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(models.UserSocialMedia)
class UserSocialMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'social_media_type', 'social_media_link')
    list_display_links = ('id', 'user')
    list_filter = ('user', 'social_media_type')
    search_fields = ('user', 'social_media_type', 'social_media_link')