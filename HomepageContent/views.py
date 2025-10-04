from rest_framework import generics
from .models import (
    HeaderBanner,
    MiddleBanner,
    VideoSection,
    Middle_2_Banner,
    WayToSuccess,
)
from .serilizers import (
    HeaderBannerSerializer,
    MiddleBannerSerializer,
    VideoSectionSerializer,
    Middle2BannerSerializer,
    WayToSuccessSerializer,
)


class HeaderBannerView(generics.ListAPIView):
    serializer_class = HeaderBannerSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return HeaderBanner.objects.filter(show=True)


class MiddleBannerView(generics.ListAPIView):
    serializer_class = MiddleBannerSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return MiddleBanner.objects.filter(show=True)


class VideoSectionView(generics.ListAPIView):
    serializer_class = VideoSectionSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return VideoSection.objects.filter(show=True)


class Middle2BannerView(generics.ListAPIView):
    serializer_class = Middle2BannerSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Middle_2_Banner.objects.filter(show=True)


class WayToSuccessView(generics.ListAPIView):
    serializer_class = WayToSuccessSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return WayToSuccess.objects.filter(show=True)
