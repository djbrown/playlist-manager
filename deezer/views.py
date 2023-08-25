import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from deezer.models import Playlist, find_multiplaylist_tracks


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

    params = {
        "app_id": settings.DEEZER_APP_ID,
        "secret": settings.DEEZER_SECRET_KEY,
        "code": code,
        "output": "json",
    }
    token_link = "https://connect.deezer.com/oauth/access_token.php"
    token_response = requests.get(token_link, params, timeout=5)
    token_json = token_response.json()

    response = HttpResponseRedirect("/deezer/")
    response.set_cookie(
        "deezer_access_token",
        token_json["access_token"],
        max_age=token_json["expires"],
    )
    return response


def playlists(request: HttpRequest):
    context = {"playlists": Playlist.objects.all()}
    return render(request, "deezer/playlists.html", context)


def duplicates(request: HttpRequest):
    tracks = find_multiplaylist_tracks()
    context = {"tracks": tracks}
    return render(request, "deezer/duplicates.html", context)
