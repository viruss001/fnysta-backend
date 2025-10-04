from django.db import models
from profiles.models import Profiles
# Create your models here.
class CouponCode(models.Model):
    code = models.CharField(max_length=50)
    discount = models.IntegerField(default=5)
    active = models.BooleanField(default=False)
    exp = models.DateField()

class UsedCode(models.Model):
    code = models.ManyToManyField(CouponCode)
    user = models.ManyToManyField(Profiles)
    