from django.urls import path
from apps.beauty_center import views

urlpatterns = [
    path("", views.BeautyCenterListView.as_view(), name="beauty_centers"),
    path("<slug:slug>/doctor/", views.BeautyCenterDoctorListView.as_view(), name="beauty_center_doctors"),
]
