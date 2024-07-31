import random

from django.conf import settings
from django.core.mail import send_mail


def generate_confirmation_code():
    return random.randint(100_000, 999_999)


def send_confirmation_email(email, confirmation_code):
    subject = 'Your confirmation code'
    message = f'Your confirmation code is {confirmation_code}'
    email_from = settings.EMAIL_FROM
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
