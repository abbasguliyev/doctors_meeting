from django.contrib import admin
from apps.hospital import models

@admin.register(models.Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'city', 'address', 'phone')
    list_display_links = ('id', 'name')
    list_filter = ('id', 'name', 'country', 'city', 'address', 'phone')
    search_fields = ('id', 'name')
    prepopulated_fields = {"slug": ["name"]}