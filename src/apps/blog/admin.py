from django.contrib import admin
from apps.blog.models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'author', 'content', 'create_at', 'update_at')
    list_display_links = ('id', 'title', 'slug')
    list_filter = ('id', 'title', 'author', 'create_at', 'update_at')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ["title"]}