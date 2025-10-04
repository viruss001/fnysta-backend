from django.urls import path
from .HomePageViews import (
    create_header_banner, update_header_banner, delete_header_banner,
    create_middle_banner, update_middle_banner, delete_middle_banner,
    create_video_section, update_video_section, delete_video_section,
    create_middle2_banner, update_middle2_banner, delete_middle2_banner,
    create_way_to_success, update_way_to_success, delete_way_to_success,
)

urlpatterns = [
    # HeaderBanner
    path('header-banner/create/', create_header_banner, name='create_header_banner'),
    path('header-banner/update/<int:pk>/', update_header_banner, name='update_header_banner'),
    path('header-banner/delete/<int:pk>/', delete_header_banner, name='delete_header_banner'),

    # MiddleBanner
    path('middle-banner/create/', create_middle_banner, name='create_middle_banner'),
    path('middle-banner/update/<int:pk>/', update_middle_banner, name='update_middle_banner'),
    path('middle-banner/delete/<int:pk>/', delete_middle_banner, name='delete_middle_banner'),

    # VideoSection
    path('video-section/create/', create_video_section, name='create_video_section'),
    path('video-section/update/<int:pk>/', update_video_section, name='update_video_section'),
    path('video-section/delete/<int:pk>/', delete_video_section, name='delete_video_section'),

    # Middle_2_Banner
    path('middle2-banner/create/', create_middle2_banner, name='create_middle2_banner'),
    path('middle2-banner/update/<int:pk>/', update_middle2_banner, name='update_middle2_banner'),
    path('middle2-banner/delete/<int:pk>/', delete_middle2_banner, name='delete_middle2_banner'),

    # WayToSuccess
    path('way-to-success/create/', create_way_to_success, name='create_way_to_success'),
    path('way-to-success/update/<int:pk>/', update_way_to_success, name='update_way_to_success'),
    path('way-to-success/delete/<int:pk>/', delete_way_to_success, name='delete_way_to_success'),
]
