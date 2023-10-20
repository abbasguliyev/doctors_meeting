from django.contrib import admin

from apps.pages.models import Contact, Ads, AdsComment, AdsReport, AdsClick, News, Conference


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'subject', 'phone', 'message')
    list_display_links = ('id', 'email')
    list_filter = ('id', 'subject')
    search_fields = ('id', 'email', 'name')

@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'is_active', 'created_at', 'updated_at')
    list_display_links = ('id', 'slug', 'title')
    list_filter = ('id', 'title', 'is_active', 'created_at', 'updated_at')
    search_fields = ('id', 'title', 'slug')
    prepopulated_fields = {"slug": ["title"]}

@admin.register(AdsComment)
class AdsCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'ads', 'comment', 'created_at', 'updated_at')
    list_display_links = ('id',)
    list_filter = ('id', 'owner', 'ads', 'created_at', 'updated_at')
    search_fields = ('id', 'owner', 'ads', 'comment')

@admin.register(AdsReport)
class AdsReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'ads', 'women_count', 'man_count', 'total_count', 'age_range', 'report_date')
    list_display_links = ('id', 'ads')
    list_filter = ('ads', 'report_date')
    search_fields = ('ads', 'report_date')

@admin.register(AdsClick)
class AdsClickAdmin(admin.ModelAdmin):
    list_display = ('id', 'ads', 'user', 'click_date')
    list_display_links = ('id', 'ads', 'user')
    list_filter = ('ads', 'user', 'click_date')
    search_fields = ('ads', 'user', 'click_date')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'created_at', 'updated_at')
    list_display_links = ('id', 'slug', 'title')
    list_filter = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('id', 'title', 'slug')
    prepopulated_fields = {"slug": ["title"]}

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'created_at', 'updated_at')
    list_display_links = ('id', 'slug', 'title')
    list_filter = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('id', 'title', 'slug')
    prepopulated_fields = {"slug": ["title"]}

admin.site.site_header = 'Doctors Meeting Admin'
admin.site.site_title = 'adminsitration of Doctors Meeting'