from django.db import models
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from apps.authentication.models import DoctorProfile

class Blog(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=255, unique=True)
    content = RichTextField(null=True, blank=True)
    author = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="blogs")
    image = models.ImageField(upload_to='blog', blank=True, default='default-photo.png', validators=[FileExtensionValidator(['jpg','jpeg','png',])])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title