from django.contrib import admin
from .models import Profiles,Coins,BirthDetails,UserLoggedIn
# Register your models here.
admin.site.register(Profiles)
admin.site.register(Coins)
admin.site.register(BirthDetails)
admin.site.register(UserLoggedIn)
