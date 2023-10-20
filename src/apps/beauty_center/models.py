from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField

class BeautyCenter(models.Model):
    name = models.CharField(max_length=255)
    about = RichTextField(blank=True)
    image = models.ImageField(upload_to='beauty_center/image_upload', blank=True, default='beauty_center_default.png', validators=[FileExtensionValidator(['jpg','jpeg', 'gif', 'png',])])
    country= models.CharField(max_length=255, null=True, blank=True)
    city= models.CharField(max_length=255, null=True, blank=True)
    address= models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name
    
class BeautyCenterStaff(models.Model):
    beauty_center = models.ForeignKey(BeautyCenter, on_delete=models.CASCADE, related_name="beauty_center_staff")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="beauty_center_staff")
