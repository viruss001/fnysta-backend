from django.urls import path
from .views import astroapp_today_api,astroapp_week_api,astroapp_month_api,astroapp_year_api

urlpatterns = [
    path('today/', astroapp_today_api, name='astroapp_api'),
    path('weekly/', astroapp_week_api, name='astroapp_week_api'),
    path('monthly/', astroapp_month_api, name='astroapp_month_api'),
    path('yearly/', astroapp_year_api, name='astroapp_year_api'),
   
]
