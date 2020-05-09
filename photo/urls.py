from django.urls import path
from photo import views
from django.contrib.auth.decorators import login_required

app_name="photo"

urlpatterns = [
    path("", login_required(views.PhotoList.as_view()), name="list"),
    path("detail/<int:pk>", views.PhotoDetail.as_view(), name="detail"),
    path("create/", views.PhotoCreate.as_view(), name="create"),
]