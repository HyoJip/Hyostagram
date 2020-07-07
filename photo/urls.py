from django.urls import path
from photo import views
from django.contrib.auth.decorators import login_required

app_name = "photo"

urlpatterns = [
    # Photo
    path("", login_required(views.PhotoList.as_view()), name="list"),
    path("create/", views.PhotoCreate.as_view(), name="create"),
    path("detail/<int:pk>/", views.PhotoDetail.as_view(), name="detail"),
    path("update/<int:pk>/", views.PhotoUpdate.as_view(), name="update"),
    path("delete/<int:pk>/", views.PhotoDelete.as_view(), name="delete"),


    # Comment
    path("comment/create/<int:photo_pk>/",
         views.CommentCreate.as_view(), name="comment_create"),
    path("comment/create/ajax/<int:pk>/",
         views.CommentCreateAjaxView.as_view(), name="comment_create_ajax"),
    path("comment/update/<int:pk>/",
         views.CommentUpdate.as_view(), name="comment_update"),
    path("comment/delete/<int:pk>/",
         views.CommentDelete.as_view(), name="comment_delete"),

    # LikeAjax
    path("like/", views.photo_like, name="photo_like"),
    path("like/comment", views.comment_like, name="comment_like"),
]
