from django.urls import path
from .views import SendOtpView, VerifyOtpView,LogoutUser,SendOtpView2

urlpatterns = [
    path('send-otp/', SendOtpView.as_view(), name='send_otp'),
    path('send-otp2/', SendOtpView2.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('logout/',LogoutUser , name='logout'),
]
