from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    about = RichTextField(blank=True)
    image = models.ImageField(upload_to='hospitals/image_upload', blank=True, default='default-hospital.jpg', validators=[FileExtensionValidator(['jpg','jpeg', 'gif', 'png',])])
    country= models.CharField(max_length=255, null=True, blank=True)
    city= models.CharField(max_length=255, null=True, blank=True)
    address= models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

class HospitalStaff(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="hospital_staff")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="hospital_staff")
