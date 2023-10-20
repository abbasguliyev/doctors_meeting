from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from apps.appointment.models import Availability, AppointmentRequest, AppointmentRequestFile

def availability_list() -> QuerySet[Availability]:
    qs = Availability.objects.select_related('available_user').all()
    return qs

def appointment_request_list() -> QuerySet[AppointmentRequest]:
    qs = AppointmentRequest.objects.select_related('doctor', 'owner').all()
    return qs

def appointment_request_file_list() -> QuerySet[AppointmentRequestFile]:
    qs = AppointmentRequestFile.objects.select_related('appointment_request', 'patient_file').all()
    return qs