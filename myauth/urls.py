from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    AboutMeView,
    RegisterView,
    ProfileUpdateView,
    UsersListView,
    UserDetailView,
)

app_name = "myauth"

urlpatterns = [
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("login/", LoginView.as_view(template_name="myauth/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page='myauth:login'), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<int:user_id>/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("users/", UsersListView.as_view(), name="users_list"),
    path("users/<int:user_id>/", UserDetailView.as_view(), name="user_detail"),
]