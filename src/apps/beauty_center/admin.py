from django.contrib import admin
from apps.beauty_center import models

@admin.register(models.BeautyCenter)
class BeautyCenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'address', 'phone')
    list_display_links = ('id', 'name')
    list_filter = ('id', 'name', 'country', 'address', 'phone')
    search_fields = ('id', 'name')
    prepopulated_fields = {"slug": ["name"]}