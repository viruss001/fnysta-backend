from django.db import models
from django.utils import timezone
from datetime import timedelta

def default_expiry():
    return timezone.now() + timedelta(minutes=20)

class Otp(models.Model):
    otp = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    exp = models.DateTimeField(default=default_expiry)  # use DateTimeField for exact expiry

    def is_expired(self):
        return timezone.now() > self.exp
