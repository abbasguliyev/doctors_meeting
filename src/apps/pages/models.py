from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self) -> str:
        return self.subject
    
class Ads(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    ads_image = models.FileField(upload_to='advertisement', null=True, blank=True, validators=[FileExtensionValidator(['jpg','jpeg','png', 'svg'])])
    description = RichTextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ads"
        verbose_name_plural = "Ads"

    def __str__(self) -> str:
        return self.title
    
class AdsComment(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="ads_comments")
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.comment[:20]}"

class AdsReport(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name="reports")
    women_count = models.PositiveBigIntegerField(default=0)
    man_count = models.PositiveBigIntegerField(default=0)
    total_count = models.PositiveBigIntegerField(default=0)
    age_range = models.CharField(max_length=100, null=True, blank=True)
    report_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.ads.title
    
class AdsClick(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name="ads_click")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="ads_click")
    click_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.email} clicked {self.ads.title}"

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    news_image = models.FileField(upload_to='news', default='default-photo.png', blank=True, validators=[FileExtensionValidator(['jpg','jpeg','png', 'svg'])])
    content = RichTextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

class Conference(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    conf_image = models.FileField(upload_to='conference', default='default-photo.png', blank=True, validators=[FileExtensionValidator(['jpg','jpeg','png', 'svg'])])
    content = RichTextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title