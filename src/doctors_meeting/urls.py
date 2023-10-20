"""
URL configuration for doctors_meeting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns
from apps.pages.views import set_language

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', include('apps.pages.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('appointment/', include('apps.appointment.urls')),
    path('hospital/', include('apps.hospital.urls')),
    path('beauty-center/', include('apps.beauty_center.urls')),
    path('blog/', include('apps.blog.urls')),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
    path("set_language/<str:language>", set_language, name="set-language"),
]