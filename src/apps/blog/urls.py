from django.urls import path
from django.contrib.auth import views as auth_views
from apps.blog import views


urlpatterns = [
     path("doctor/", views.ProfileBlogView.as_view(), name="profile_blog"),
     path("doctor/add-blog/", views.ProfileBlogCreateView.as_view(), name="profile_blog_create"),
     path("doctor/<slug:slug>/", views.ProfileBlogDetailView.as_view(), name="profile_blog_detail"),
     path("doctor/blog_delete/<slug:slug>/", views.ProfileBlogDeleteView.as_view(), name="profile_blog_delete"),
     
     path("doctor-blog/<int:pk>/", views.DoctorBlogView.as_view(), name="doctor_blog"),

     path("", views.BlogView.as_view(), name="blog"),
     path("<slug:slug>/", views.BlogDetailView.as_view(), name="blog-detail"),
]
