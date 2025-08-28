
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="new"),
    path("profile/<str:creator>", views.P, name="profile"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),

    # api route
    path("like/<int:post_id>", views.like, name="like"),
    path("profile/like/<int:post_id>", views.like, name="like"),



  
]
