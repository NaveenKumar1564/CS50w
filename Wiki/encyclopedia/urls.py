from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path ("wiki/<str:entry>", views.get_page, name="Title"),
    path("Create", views.New_Page, name="Create"),
    path("Search", views.search, name="search"),
    path("random", views.random_page, name="Random"),
    path("wiki/<str:entry>/edit", views.edit, name="edit")

]
