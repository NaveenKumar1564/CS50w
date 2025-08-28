
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("AddNewAudio", views.new_audio, name="create"),
    path("Albums", views.Albums, name="Albums"),
    path("albums/<str:album>", views.album_view, name="show"),
    path("likedsongs", views.Liked, name="liked"),
    path("song/<int:song_id>", views.song, name="song"),

    # api route
    path("like/<int:song_id>", views.like, name="like"),
    
]
