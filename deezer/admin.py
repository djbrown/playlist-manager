from django.contrib import admin

from deezer.models import Playlist, Track


admin.site.register(Playlist)
admin.site.register(Track)
