import datetime
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField

from apps.authentication.enums import Title, CurrencyUnit, DoctorAcceptedStatus, UserType, GenderOptions, SocialMediaType

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(
        choices=UserType.choices, max_length=155, null=True, blank=True
    )
    phone_number = PhoneNumberField(blank=True)
    gender = models.CharField(choices=GenderOptions.choices, default=GenderOptions.MALE, max_length=20)
    birth_date = models.DateField(blank=True, null=True)
    id_card = models.FileField(upload_to='doctors/id_card_upload', null=True, blank=True)
    is_online = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ('id',)

    @property
    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name
   
class Profession(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Professions"

    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    currency_unit = models.CharField(choices=CurrencyUnit.choices, max_length=6, blank=True, null=True)
    about_doctor = RichTextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='doctors/avatar_upload', blank=True, default='default-photo.png', validators=[FileExtensionValidator(['jpg','jpeg', 'gif', 'png',])])
    country= models.ForeignKey('cities_light.Country', related_name='profile', on_delete=models.SET_NULL, null=True, blank=True)
    city= models.ForeignKey('cities_light.City', related_name='profile', on_delete=models.SET_NULL, null=True, blank=True)
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, related_name='profile', null=True, blank=True)
    title = models.CharField(choices=Title.choices, max_length=30, null=True, blank=True)
    orcid_account = models.URLField(max_length=200, null=True, blank=True)
    pubmed_account = models.URLField(max_length=200, null=True, blank=True)
    hospital = models.ForeignKey("hospital.Hospital", on_delete=models.SET_NULL, null=True, blank=True, related_name="doctors")
    beauty_center = models.ForeignKey("beauty_center.BeautyCenter", on_delete=models.SET_NULL, null=True, blank=True, related_name="doctors")
    status = models.CharField(
        choices=DoctorAcceptedStatus.choices, default=DoctorAcceptedStatus.waiting, max_length=100
    )
    slug = models.SlugField(max_length=255, unique=True)
    diseases = models.ManyToManyField(Disease, related_name="doctors", blank=True)

    def get_absolute_url(self):
        return reverse("doctor-detail", kwargs={"slug": self.slug})
    
    def __str__(self) -> str:
        return self.user.email
    

class Experience(models.Model):
    user = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='experience',null=True)
    experience_place = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    city = models.CharField(max_length=255, null=True, blank=True)
    start_year = models.PositiveIntegerField(('start_year'), validators=[MinValueValidator(0), MaxValueValidator(datetime.date.today().year)], default=datetime.datetime.now().year)
    end_year = models.PositiveIntegerField(('end_year'), validators=[MinValueValidator(0), MaxValueValidator(datetime.date.today().year)], null=True, blank=True)
    is_continue = models.BooleanField(default=False)


class Education(models.Model):
    user = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='education')
    education_place = models.CharField(max_length=100)
    education_branch = models.CharField(max_length=100)
    city = models.CharField(max_length=255, null=True, blank=True)
    start_year = models.PositiveIntegerField(('start_year'), validators=[MinValueValidator(0), MaxValueValidator(datetime.date.today().year)], default=datetime.datetime.now().year)
    end_year = models.PositiveIntegerField(('end_year'), validators=[MinValueValidator(0), MaxValueValidator(datetime.date.today().year)], null=True, blank=True)
    is_continue = models.BooleanField(default=False)


class UserSocialMedia(models.Model):
    user = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='social_medias')
    social_media_type = models.CharField(max_length=500, choices=SocialMediaType.choices)
    social_media_link = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.social_media_type

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')

class PatientsFile(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="patient_files")
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True)
    patient_file = models.FileField(upload_to='patient/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.name