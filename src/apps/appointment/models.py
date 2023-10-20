from django.db import models
from django.contrib.postgres.fields import ArrayField, DateTimeRangeField
from django.contrib.auth import get_user_model
from apps.appointment.enums import DoctorsRequest, StatusOption
from apps.authentication.models import PatientsFile
from ckeditor.fields import RichTextField

class Availability(models.Model):
    available_start_time = models.DateTimeField()
    available_end_time = models.DateTimeField()
    reserved = models.BooleanField(default=False)
    available_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='available_user')

    def __str__(self):
        return f"{self.available_user}->{self.available_start_time} - {self.available_end_time}"

class AppointmentRequest(models.Model):
    doctor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="doctor")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="owner")
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, related_name="appointment_request")
    appointment_date = models.DateTimeField()
    doctor_request = models.CharField(choices=DoctorsRequest.choices, default=DoctorsRequest.WAITING,max_length=20)
    request_status = models.CharField(choices=StatusOption.choices, default=StatusOption.ACTIVE, max_length=20)
    explanation = models.CharField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)

class AppointmentRequestFile(models.Model):
    appointment_request = models.ForeignKey(AppointmentRequest, on_delete=models.CASCADE, related_name="files")
    patient_file = models.ForeignKey(PatientsFile, on_delete=models.CASCADE, related_name="appointment_requests")
    is_downloaded = models.BooleanField(default=False)


class Meeting(models.Model):
    appointment_request = models.ForeignKey(AppointmentRequest, on_delete=models.CASCADE, related_name="meeting")
    room_name = models.CharField(max_length=255)
    doctor = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="doctor_meeting")
    patient = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="patient_meeting")
    meet_record = models.FileField(upload_to="meeting/%Y/%m/%d/", null=True, blank=True)
    meet_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.room_name
    

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class DoctorNote(models.Model):
    doctor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="doctor_note")
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, related_name="meeting_note")
    note = RichTextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.doctor.first_name} {self.doctor.last_name}"
