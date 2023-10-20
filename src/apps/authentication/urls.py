from django.urls import path
from django.contrib.auth import views as auth_views
from apps.authentication import views


urlpatterns = [
     path('activate/<uidb64>/<token>', views.activate, name='activate'),
     path("login/", views.LoginView.as_view(), name="login"),
     path("register/", views.RegisterUserView.as_view(), name="register"),
     path("register/doctor-register/", views.RegisterDoctorView.as_view(), name="doctor_register"),
     path("logout/", views.LogoutView.as_view(), name="logout"),

     path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
     path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
     
     path('profile/change-password/', views.ChangePasswordView.as_view(), name='change_password'),

     path('profile/social-media/', views.UserSocialMediaListView.as_view(), name='social_media'),
     path('profile/social-media-create/', views.UserSocialMediaCreateView.as_view(), name='social_media_create'),
     path('profile/social-media/<int:pk>/', views.UserSocialMediaDetailView.as_view(), name='social_media_detail'),
     path('profile/social-media-delete/<int:pk>/', views.UserSocialMediaDeleteView.as_view(), name='social_media_delete'),
     
     path("profile/experience/", views.ExperienceListView.as_view(), name="experience"),
     path("profile/experience/<int:pk>/", views.ExperienceDetailView.as_view(), name="experience_detail"),
     path("profile/experience-delete/<int:pk>/", views.ExperienceDeleteView.as_view(), name="experience_delete"),
     path("profile/experience-create/", views.ExperienceCreateView.as_view(), name="experience_create"),

     path("profile/education/", views.EducationListView.as_view(), name="education"),
     path("profile/education/<int:pk>/", views.EducationDetailView.as_view(), name="education_detail"),
     path("profile/education-delete/<int:pk>/", views.EducationDeleteView.as_view(), name="education_delete"),
     path("profile/education-create/", views.EducationCreateView.as_view(), name="education_create"),

     path("profile/patient-file/", views.PatientFileListView.as_view(), name="patient_files"),
     path("profile/patient-file/<int:pk>/", views.PatientFileDetailView.as_view(), name="patient_file_detail"),
     path("profile/patient-file-delete/<int:pk>/", views.PatientFileDeleteView.as_view(), name="patient_file_delete"),
     path("profile/patient-file-add/", views.PatientFileCreateView.as_view(), name="patient_file_add"),

     path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
     path("profile-update/<int:pk>/", views.ProfileUpdateView.as_view(), name="profile_update"),
     
     path("doctors/", views.DoctorListView.as_view(), name="doctors"),
     path("doctors/<slug:slug>/", views.DoctorDetailView.as_view(), name="doctor_detail"),

     path('load-cities/', views.load_cities, name='load_cities'),
]
