
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post", views.post, name="post"),
    path("<int:user_id>", views.profile, name="profile"),
    path("<int:user_id>/follow", views.follow, name="follow"),
    path("<int:user_id>/unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # API Routes
    path("edit/<int:post_id>", views.edit_post, name="edit"),
    path("like/<int:post_id>", views.like_post, name="like")
]
