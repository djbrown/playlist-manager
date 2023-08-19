import requests
from django.core.management.base import BaseCommand, CommandError

from deezer.models import Playlist, Track


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("token")

    def handle(self, *_, **options):
        params = {"access_token": options["token"], "limit": "100"}

        playlists_link = "https://api.deezer.com/user/me/playlists"
        playlists_response: dict = requests.get(playlists_link, params, timeout=5)
        playlists_json = playlists_response.json()

        if "error" in playlists_json:
            raise CommandError(playlists_json["error"])

        total = playlists_json["total"]
        self.stdout.write(f"Importing {total} Playlists ", ending="")

        for p_json in playlists_json["data"]:
            playlist_link = p_json["link"]
            (playlist, _) = Playlist.objects.update_or_create(
                link=playlist_link,
                defaults={
                    "title": p_json["title"],
                    "link": playlist_link,
                },
            )

            self.stdout.write(".", ending="")

            tracks_link = p_json["tracklist"]
            tracks_response = requests.get(tracks_link, params, timeout=5)
            tracks_json = tracks_response.json()

            tracks: list[Track] = []
            for track_json in tracks_json["data"]:
                track_link = track_json["link"]
                (track, _) = Track.objects.update_or_create(
                    link=track_link,
                    defaults={
                        "title": track_json["title"],
                        "link": track_link,
                    },
                )
                tracks.append(track)
            playlist.tracks.set(tracks)

        self.stdout.write("")
        self.stdout.write("========DONE========")
