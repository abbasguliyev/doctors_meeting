from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from apps.authentication import selectors
from apps.appointment import selectors as appointment_selectors

def appointment_request_mail(user_id, message):
    user = selectors.user_list().filter(pk=user_id).last()
    if user is not None:
        to_email = user.email
        mail_subject = 'Appointment Request.'
        message = render_to_string('appointment-mail/appointment_request_mail.html', {
            'user': user,
            'message' : f"{message}"
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

def appointment_request_accepted_mail(user_id, instance):
    appointment_request = appointment_selectors.appointment_request_list().filter(pk=instance).last()
    user = selectors.user_list().filter(pk=user_id).last()
    if user is not None:
        to_email = user.email
        mail_subject = 'Appointment Request.'
        message = render_to_string('appointment-mail/appointment_request_accepted_mail.html', {
            'user': user,
            'message' : f"Your Appointment Request accepted by doctor. Appointment date: {appointment_request.appointment_date}"
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

def appointment_reminder():
    now = timezone.now()
    apt_reqs = appointment_selectors.appointment_request_list()
    for apt_req in apt_reqs:
        apt_date = apt_req.appointment_date
        difference = apt_date - now
        if int(difference.days) <= 3 and int(difference.days) == 0:
            doctor = apt_req.doctor
            owner = apt_req.owner
            appointment_request_mail(doctor.id, f"You have appointment with {owner.first_name} {owner.last_name} in {apt_date}")
            appointment_request_mail(owner.id, f"You have appointment with {doctor.first_name} {doctor.last_name} in {apt_date}")

def send_appointment_file_downloaded_reminder():
    now = timezone.now()
    apt_req_files = appointment_selectors.appointment_request_file_list()
    for apt_req_file in apt_req_files:
        apt_req = apt_req_file.appointment_request
        apt_date = apt_req.appointment_date
        difference = apt_date - now
        if int(difference.days) <= 7 and int(difference.days) == 0:
            doctor = apt_req.doctor
            owner = apt_req.owner
            appointment_request_mail(doctor.id, f"You did not downloaded patient {owner.first_name} {owner.last_name} file yet. Your appointment date is {apt_req.appointment_date}")
