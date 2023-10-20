from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from apps.authentication.models import Profession, Experience, Education, DoctorProfile, PatientProfile, Disease, PatientsFile
from cities_light.models import Country, City


def user_list() -> QuerySet[get_user_model()]:
    qs = get_user_model().objects.prefetch_related('groups', 'user_permissions').all()
    return qs

def city_list() -> QuerySet[City]:
    qs = City.objects.select_related('country', 'subregion', 'region').all()
    return qs

def country_list() -> QuerySet[Country]:
    qs = Country.objects.all()
    return qs

def profession_list() -> QuerySet[Profession]:
    qs = Profession.objects.all()
    return qs


def experience_list() -> QuerySet[Experience]:
    qs = Experience.objects.select_related('user').all()
    return qs


def education_list() -> QuerySet[Education]:
    qs = Education.objects.select_related('user').all()
    return qs

def doctor_profile_list() -> QuerySet[DoctorProfile]:
    qs = DoctorProfile.objects.select_related('user', 'country', 'city', 'profession').all()
    return qs

def patient_profile_list() -> QuerySet[PatientProfile]:
    qs = PatientProfile.objects.select_related('user').all()
    return qs

def disease_list() -> QuerySet[Disease]:
    qs = Disease.objects.all()
    return qs

def patient_file_list() -> QuerySet[PatientsFile]:
    qs = PatientsFile.objects.select_related('patient').all()
    return qs