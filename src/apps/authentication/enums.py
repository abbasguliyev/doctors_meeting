from django.db import models
from django.utils.translation import gettext_lazy as _    


class Title(models.TextChoices):
    PROFESSOR_DOCTOR = "professor doctor", _("Professor Doctor")
    ASSOCIATE_PROFESSOR = "associate professor", _("Associate Professor")
    SPECIALIST = "specialist", _("Specialist")
    LECTURER = "lecturer", _("Lecturer")


class CurrencyUnit(models.TextChoices):
    DOLLAR = "dollar", ("$")
    EURO = "euro", ("€")
    TL = "tl", ("₺")

class DoctorAcceptedStatus(models.TextChoices):
    accepted = "Accepted", _("Accepted")
    rejected = "Rejected", _("Rejected")
    waiting = "Waiting", _("Waiting")

class UserType(models.TextChoices):
    patient = "Patient", _("Patient")
    doctor = "Doctor", _("Doctor")
    health_representative = "Health Representative", _("Health Representative")


class GenderOptions(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")

class SocialMediaType(models.TextChoices):
    FACEBOOK = "facebook", _("Facebook")
    INSTAGRAM = "instagram", _("Instagram")
    LINKEDIN = "linkedin", _("Linkedin")
    TWITTER = "twitter", _("Twitter")