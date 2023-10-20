from django.urls import path
from apps.hospital import views

urlpatterns = [
    path("", views.HospitalListView.as_view(), name="hospitals"),
    path("<slug:slug>/doctor/", views.HospitalDoctorListView.as_view(), name="hospital_doctors"),
    path("<slug:slug>/", views.HospitalDetailView.as_view(), name="hospital_detail"),
]
