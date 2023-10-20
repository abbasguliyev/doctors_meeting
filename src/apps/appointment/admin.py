from django.contrib import admin
from apps.appointment.models import Availability, AppointmentRequest, AppointmentRequestFile, Meeting, RoomMember, DoctorNote

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'available_start_time', 'available_end_time', 'reserved', 'available_user')
    list_display_links = ('id', 'available_start_time', 'available_end_time')
    list_filter = ('available_user',)

@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'doctor', 'appointment_date', 'doctor_request', 'request_status', 'explanation', 'create_at')
    list_display_links = ('id', 'owner')
    list_filter = ('owner', 'doctor', 'doctor_request', 'request_status', 'create_at')

@admin.register(AppointmentRequestFile)
class AppointmentRequestFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment_request', 'patient_file', 'is_downloaded')
    list_display_links = ('id', 'appointment_request', 'patient_file')
    list_filter = ('appointment_request', 'patient_file', 'is_downloaded')
    search_fields = ('appointment_request', 'patient_file')

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_name', 'doctor', 'patient', 'appointment_request', 'active')
    list_display_links = ('id', 'room_name')
    list_filter = ('room_name', 'doctor', 'patient')
    search_fields = ('room_name', 'doctor', 'patient', 'appointment_request')

@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uid', 'room_name', 'insession')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'room_name')
    search_fields = ('name', 'room_name')

@admin.register(DoctorNote)
class DoctorNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'meeting')
    list_display_links = ('id', 'doctor', 'meeting')
    list_filter = ('doctor', 'meeting')