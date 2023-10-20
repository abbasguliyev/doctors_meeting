from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib import messages
from apps.authentication.tokens import account_activation_token
from apps.authentication import selectors

def activateEmail(domain, is_secure, user_id, to_email):
    user = selectors.user_list().filter(pk=user_id).last()
    if user is not None:
        mail_subject = 'Activate your user account.'
        message = render_to_string('mail-activation/template_activate_account.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if is_secure else 'http'
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

def do_offline(user):
    user.is_online = False
    user.save()
    return user

def do_online(user):
    user.is_online = True
    user.save()
    return user