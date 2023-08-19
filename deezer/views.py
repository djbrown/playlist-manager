import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from .models import Playlist


def index(request):
    return render(request, "deezer/index.html")


def login(request: HttpRequest):
    context = {
        "DEEZER_APP_ID": settings.DEEZER_APP_ID,
        "DEEZER_CALLBACK_URL": settings.DEEZER_CALLBACK_URL,
    }
    return render(request, "deezer/login.html", context)


def callback(request: HttpRequest):
    code = request.GET.get("code")

    token_response = requests.get(
        "https://connect.deezer.com/oauth/access_token.php",
        params={
            "app_id": settings.DEEZER_APP_ID,
            "secret": settings.DEEZER_SECRET_KEY,
            "code": code,
            "output": "json",
        },
    ).json()

    response = HttpResponseRedirect("/deezer/")
    response.set_cookie(
        "deezer_access_token",
        token_response["access_token"],
        max_age=token_response["expires"],
    )
    return response


def playlists(request: HttpRequest):
    context = {"playlists": Playlist.objects.all()}
    return render(request, "deezer/playlists.html", context)
