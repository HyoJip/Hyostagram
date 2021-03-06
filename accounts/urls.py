from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

app_name = "accounts"
urlpatterns = [

    # auth_views
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("account/logout/",
         auth_views.LogoutView.as_view(), name="logout"),

    # Accounts App views
    path("signup/", views.UserCreate.as_view(), name="signup"),
    path("signup/done/", views.UserRegistered.as_view(), name="create_user_done"),

    # Profile views
    path("profile/update", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/<slug:slug>/", views.ProfileView.as_view(), name="profile"),
    path("profile/<slug:slug>/follow/", views.follow, name="user_follow"),

    path("profile/<slug:slug>/photo_like/",
         views.UserLikePhoto.as_view(), name="user_like_photo"),
    path("search/", views.SearchUser.as_view(), name="search_result"),
]
