from django.db import models

# Create your models here.
class HeaderBanner(models.Model):
    banner = models.ImageField(upload_to="homepage/headerBanner")
    show = models.BooleanField(default=False)

class MiddleBanner(models.Model):
    banner = models.ImageField(upload_to="homepage/middleBanner")
    show = models.BooleanField(default=False)
    
class VideoSection(models.Model):
    video = models.FileField(upload_to="homepage/VideoSection")
    show = models.BooleanField(default=False)

class Middle_2_Banner(models.Model):
    banner = models.ImageField(upload_to="homepage/middle_2_Banner")
    show = models.BooleanField(default=False)
    
class WayToSuccess(models.Model):
    img = models.ImageField(upload_to="homepage/middleBanner")
    show = models.BooleanField(default=False)