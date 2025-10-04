from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from HomepageContent.models import (
    HeaderBanner,
    MiddleBanner,
    VideoSection,
    Middle_2_Banner,
    WayToSuccess,
)
from HomepageContent.serilizers import (
    HeaderBannerSerializer,
    MiddleBannerSerializer,
    VideoSectionSerializer,
    Middle2BannerSerializer,
    WayToSuccessSerializer,
)

# Custom authentication disables CSRF
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # disables CSRF check

# -----------------------------
# HeaderBanner
# -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def create_header_banner(request):
    serializer = HeaderBannerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def update_header_banner(request, pk):
    banner = get_object_or_404(HeaderBanner, pk=pk)
    serializer = HeaderBannerSerializer(banner, data=request.data, partial=('PATCH' in request.method))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_header_banner(request, pk):
    banner = get_object_or_404(HeaderBanner, pk=pk)
    banner.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# -----------------------------
# MiddleBanner
# -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def create_middle_banner(request):
    serializer = MiddleBannerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def update_middle_banner(request, pk):
    banner = get_object_or_404(MiddleBanner, pk=pk)
    serializer = MiddleBannerSerializer(banner, data=request.data, partial=('PATCH' in request.method))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_middle_banner(request, pk):
    banner = get_object_or_404(MiddleBanner, pk=pk)
    banner.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# -----------------------------
# VideoSection
# -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def create_video_section(request):
    serializer = VideoSectionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def update_video_section(request, pk):
    video = get_object_or_404(VideoSection, pk=pk)
    serializer = VideoSectionSerializer(video, data=request.data, partial=('PATCH' in request.method))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_video_section(request, pk):
    video = get_object_or_404(VideoSection, pk=pk)
    video.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# -----------------------------
# Middle_2_Banner
# -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def create_middle2_banner(request):
    serializer = Middle2BannerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def update_middle2_banner(request, pk):
    banner = get_object_or_404(Middle_2_Banner, pk=pk)
    serializer = Middle2BannerSerializer(banner, data=request.data, partial=('PATCH' in request.method))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_middle2_banner(request, pk):
    banner = get_object_or_404(Middle_2_Banner, pk=pk)
    banner.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# -----------------------------
# WayToSuccess
# -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def create_way_to_success(request):
    serializer = WayToSuccessSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def update_way_to_success(request, pk):
    success = get_object_or_404(WayToSuccess, pk=pk)
    serializer = WayToSuccessSerializer(success, data=request.data, partial=('PATCH' in request.method))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_way_to_success(request, pk):
    success = get_object_or_404(WayToSuccess, pk=pk)
    success.delete()
    return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
