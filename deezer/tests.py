from django.test import TestCase

from deezer.models import Playlist, Track, find_multiplaylist_tracks


class MultiPlaylistTracksTestCase(TestCase):
    def test_no_playlist_track(self):
        Track.objects.create(title="", link="")

        actual = find_multiplaylist_tracks()

        self.assertEqual(list(actual), [])

    def test_single_playlist_track(self):
        playlist = Playlist.objects.create(title="", link="")

        track = Track.objects.create(title="", link="")
        track.playlist_set.add(playlist)

        actual = find_multiplaylist_tracks()

        self.assertEqual(list(actual), [])

    def test_multi_playlist_track(self):
        playlist_a = Playlist.objects.create(title="", link="")
        playlist_b = Playlist.objects.create(title="", link="")

        track = Track.objects.create(title="", link="")
        track.playlist_set.add(playlist_a, playlist_b)

        actual = find_multiplaylist_tracks()

        self.assertEqual(list(actual), [track])
