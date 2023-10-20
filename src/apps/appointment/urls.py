from django.urls import path
from apps.appointment import views

urlpatterns = [
    path("profile/availability/", views.AvailabilityView.as_view(), name="availability"),
    path("profile/availability/search/<int:available_user_id>/", views.AvailabilitySearchView.as_view(), name="availability_search"),
    path("profile/availability-create/", views.AvailabilityCreateView.as_view(), name="availability_create"),
    path("profile/availability-delete/<int:pk>/", views.AvailabilityDeleteView.as_view(), name="availability_delete"),

    path("profile/appointment-request/", views.AppointmentRequestView.as_view(), name="appointment_request"),
    path("profile/appointment-request/search/", views.AppointmentRequestSearchView.as_view(), name="appointment_request_search"),
    path("appointment-request-create/<int:availability_id>/", views.AppointmentRequestCreateView.as_view(), name="appointment_request_create"),
    path("profile/appointment-request-update/<int:pk>/", views.AppointmentRequestUpdateView.as_view(), name="appointment_request_update"),

    path('room/', views.room, name="room"),
    path('get_token/', views.getToken, name="get_token"),

    path('create_member/', views.createMember, name="create_member"),
    path('get_member/', views.getMember, name="get_member"),
    path('delete_member/', views.deleteMember, name="delete_member"),

    path('profile/notes/', views.NoteView.as_view(), name="notes"),
    path('profile/note-detail/<int:pk>/', views.NoteDetailView.as_view(), name="note_detail"),
    path('profile/note-delete/<int:pk>/', views.NoteDeleteView.as_view(), name="note_delete"),
]
