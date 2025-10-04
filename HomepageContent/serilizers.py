from rest_framework import serializers
from .models import (
    HeaderBanner,
    MiddleBanner,
    VideoSection,
    Middle_2_Banner,
    WayToSuccess,
)


class HeaderBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderBanner
        fields = "__all__"


class MiddleBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiddleBanner
        fields = "__all__"


class VideoSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSection
        fields = "__all__"


class Middle2BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Middle_2_Banner
        fields = "__all__"


class WayToSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = WayToSuccess
        fields = "__all__"
