from django.db import models
from django.db.models import Count


class Track(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self) -> str:
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=255)
    tracks = models.ManyToManyField(Track)
    link = models.URLField()

    def __str__(self) -> str:
        return self.title


def find_multiplaylist_tracks() -> list[Track]:
    return list(
        Track.objects.annotate(playlist_count=Count("playlist")).filter(
            playlist_count__gt=1
        )
    )
