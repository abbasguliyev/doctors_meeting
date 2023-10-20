from celery import shared_task
from apps.appointment import utils

@shared_task(name="send_appointment_request_mail_task")
def send_appointment_request_mail_task(user_id, message):
    utils.appointment_request_mail(user_id, message)

@shared_task(name="send_appointment_request_accepted_mail_task")
def send_appointment_request_accepted_mail_task(user_id, instance):
    utils.appointment_request_accepted_mail(user_id, instance)


@shared_task(name="send_appointment_reminder_task")
def send_appointment_reminder_task():
    utils.appointment_reminder()

@shared_task(name="send_appointment_file_downloaded_reminder_task")
def send_appointment_file_downloaded_reminder_task():
    utils.send_appointment_file_downloaded_reminder()