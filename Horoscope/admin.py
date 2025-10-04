from django.contrib import admin
from .models import Horo,WeekHoro,MonthHoro
# Register your models here.

admin.site.register(Horo)
admin.site.register(WeekHoro)
admin.site.register(MonthHoro)