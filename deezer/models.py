from django.db import models


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
