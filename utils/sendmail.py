from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_otp_email_task(self, to_email, otp):
    subject = "Your OTP Code"
    message = f"Hello ,\n\nYour OTP code is: {otp}\n\nThank you!"
    mail = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
    mail.send(fail_silently=False)
    return f"OTP email sent to {to_email}"
