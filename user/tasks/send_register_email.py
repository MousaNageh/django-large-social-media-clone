from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_register_email(code, user_email):
    message = render_to_string("register_email_template.html", {"code": code})
    text_content = strip_tags(message)
    msg = EmailMultiAlternatives(
        "Social clone: Verify your email",
        text_content,
        settings.EMAIL_HOST_USER,
        [user_email],
    )
    msg.attach_alternative(message, "text/html")
    msg.send()
