import requests
from django.core.management.base import BaseCommand, CommandError

from deezer.models import Playlist, Track


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("token")

    def handle(self, *_, **options):
        params = {"access_token": options["token"], "limit": "100"}

        playlists_link = "https://api.deezer.com/user/me/playlists"
        playlists_response: dict = requests.get(playlists_link, params).json()

        if "error" in playlists_response:
            raise CommandError(playlists_response["error"])

        total = playlists_response["total"]
        self.stdout.write(f"Importing {total} Playlists ", ending="")

        for p in playlists_response["data"]:
            playlist_link = p["link"]
            (playlist, _) = Playlist.objects.update_or_create(
                link=playlist_link,
                defaults={
                    "title": p["title"],
                    "link": playlist_link,
                },
            )

            self.stdout.write(".", ending="")

            tracks_link = p["tracklist"]
            tracks_response = requests.get(tracks_link, params).json()

            tracks: list[Track] = []
            for t in tracks_response["data"]:
                track_link = t["link"]
                (track, _) = Track.objects.update_or_create(
                    link=track_link,
                    defaults={
                        "title": t["title"],
                        "link": track_link,
                    },
                )
                tracks.append(track)
            playlist.tracks.set(tracks)

        self.stdout.write("")
        self.stdout.write("========DONE========")
