from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("callback/", views.callback, name="callback"),
    path("playlists/", views.playlists, name="playlists"),
    path("duplicates/", views.duplicates, name="duplicates"),
]
