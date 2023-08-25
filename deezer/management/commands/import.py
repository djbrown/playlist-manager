import requests
from django.core.management.base import BaseCommand, CommandError

from deezer.models import Playlist, Track


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("token")

    def handle(self, *_, **options) -> None:
        params = {"access_token": options["token"], "limit": "100"}
        playlists_link = "https://api.deezer.com/user/me/playlists"
        response_json: dict = get(playlists_link, params)

        if "error" in response_json:
            raise CommandError(response_json["error"])

        total = response_json["total"]
        self.stdout.write(f"Importing {total} Playlists ", ending="")

        for playlist_json in response_json["data"]:
            playlist = parse_playlist(playlist_json)
            self.stdout.write(".", ending="")

            tracklist_link = playlist_json["tracklist"]
            tracks_json = get(tracklist_link, params)

            tracks: list[Track] = []
            for track_json in tracks_json["data"]:
                track = parse_track(track_json)
                tracks.append(track)
            playlist.tracks.set(tracks)

        self.stdout.write("")
        self.stdout.write("========DONE========")


def get(link: str, params: dict) -> dict:
    response = requests.get(link, params, timeout=5)
    return response.json()


def parse_playlist(json: dict) -> Playlist:
    link = json["link"]
    title = json["title"]
    defaults = {"title": title, "link": link}
    return Playlist.objects.update_or_create(link=link, defaults=defaults)[0]


def parse_track(json: dict) -> Track:
    link = json["link"]
    title = json["title"]
    defaults = {"title": title, "link": link}
    return Track.objects.update_or_create(link=link, defaults=defaults)[0]
