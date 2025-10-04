from django.urls import path
from .views import HeaderBannerView,MiddleBannerView,VideoSectionView,Middle2BannerView,WayToSuccessView
urlpatterns = [
    path("HeaderBannerView/",HeaderBannerView.as_view()),
    path("MiddleBannerView/",MiddleBannerView.as_view()),
    path("VideoSectionView/",VideoSectionView.as_view()),
    path("Middle2BannerView/",Middle2BannerView.as_view()),
    path("WayToSuccessView/",WayToSuccessView.as_view()),
  
]
