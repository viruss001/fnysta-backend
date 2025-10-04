# urls.py
from django.urls import path,include
from .views import LoginView,checkUser
from .News.adminNewsPost import create_article, update_article, delete_article

urlpatterns = [
    path("login/", LoginView.as_view(), name="admin-login"),
    path("check-User/", checkUser, name="check-admin"),
    path('articles/create/', create_article, name='article-create'),
    path('articles/<int:pk>/update/', update_article, name='article-update'),
    path('articles/<int:pk>/delete/', delete_article, name='article-delete'),
    path("home/",include("adminUsers.Home.urls"))
]
