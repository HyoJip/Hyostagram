from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

app_name = "accounts"
urlpatterns = [

    # auth_views
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("account_logout/",
         auth_views.LogoutView.as_view(next_page='account_login'), name="logout"),

    # Accounts App views
    path("signup/", views.UserCreate.as_view(), name="signup"),
    path("signup/done/", views.UserRegistered.as_view(), name="create_user_done"),

    # Profile views
    path("profile/<slug:slug>/", views.ProfileView.as_view(), name="profile"),
    path("profile/update", views.ProfileUpdateView.as_view(), name="profile_update"),

]
