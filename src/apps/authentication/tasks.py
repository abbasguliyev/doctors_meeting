from celery import shared_task
from apps.authentication import utils

@shared_task(name="send_activication_email_task")
def send_activication_email_task(domain, is_secure, user_id, to_email):
    utils.activateEmail(domain, is_secure, user_id, to_email)