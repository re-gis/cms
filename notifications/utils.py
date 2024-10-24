from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def send_email_notification(recipient, subject, message):
    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False
    )
