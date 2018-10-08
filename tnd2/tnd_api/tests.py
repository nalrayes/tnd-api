import unittest
from django.urls import reverse
from django.test import Client
from .models import Album, Artist, Rating, Genre
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_album(**kwargs):
    defaults = {}
    defaults["title"] = "title"
    defaults["review_release_date"] = "review_release_date"
    defaults["fav_tracks"] = "fav_tracks"
    defaults["least_fav_track"] = "least_fav_track"
    defaults["year_released"] = "year_released"
    defaults["record_company"] = "record_company"
    defaults["album_type"] = "album_type"
    defaults["spotify_link"] = "spotify_link"
    defaults["detailed_genres"] = "detailed_genres"
    defaults["youtube_link"] = "youtube_link"
    defaults["description"] = "description"
    defaults.update(**kwargs)
    if "artists" not in defaults:
        defaults["artists"] = create_artist()
    if "rating" not in defaults:
        defaults["rating"] = create_rating()
    if "genres" not in defaults:
        defaults["genres"] = create_genre()
    return Album.objects.create(**defaults)


def create_artist(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["average_rating"] = "average_rating"
    defaults.update(**kwargs)
    return Artist.objects.create(**defaults)


def create_rating(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["rating_val"] = "rating_val"
    defaults["adjective"] = "adjective"
    defaults.update(**kwargs)
    return Rating.objects.create(**defaults)


def create_genre(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults.update(**kwargs)
    return Genre.objects.create(**defaults)


class AlbumViewTest(unittest.TestCase):
    '''
    Tests for Album
    '''
    def setUp(self):
        self.client = Client()

    def test_list_album(self):
        url = reverse('tnd_api_album_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_album(self):
        url = reverse('tnd_api_album_create')
        data = {
            "title": "title",
            "review_release_date": "review_release_date",
            "fav_tracks": "fav_tracks",
            "least_fav_track": "least_fav_track",
            "year_released": "year_released",
            "record_company": "record_company",
            "album_type": "album_type",
            "spotify_link": "spotify_link",
            "detailed_genres": "detailed_genres",
            "youtube_link": "youtube_link",
            "description": "description",
            "artists": create_artist().pk,
            "rating": create_rating().pk,
            "genres": create_genre().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_album(self):
        album = create_album()
        url = reverse('tnd_api_album_detail', args=[album.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_album(self):
        album = create_album()
        data = {
            "title": "title",
            "review_release_date": "review_release_date",
            "fav_tracks": "fav_tracks",
            "least_fav_track": "least_fav_track",
            "year_released": "year_released",
            "record_company": "record_company",
            "album_type": "album_type",
            "spotify_link": "spotify_link",
            "detailed_genres": "detailed_genres",
            "youtube_link": "youtube_link",
            "description": "description",
            "artists": create_artist().pk,
            "rating": create_rating().pk,
            "genres": create_genre().pk,
        }
        url = reverse('tnd_api_album_update', args=[album.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ArtistViewTest(unittest.TestCase):
    '''
    Tests for Artist
    '''
    def setUp(self):
        self.client = Client()

    def test_list_artist(self):
        url = reverse('tnd_api_artist_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_artist(self):
        url = reverse('tnd_api_artist_create')
        data = {
            "name": "name",
            "average_rating": "average_rating",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_artist(self):
        artist = create_artist()
        url = reverse('tnd_api_artist_detail', args=[artist.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_artist(self):
        artist = create_artist()
        data = {
            "name": "name",
            "average_rating": "average_rating",
        }
        url = reverse('tnd_api_artist_update', args=[artist.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class RatingViewTest(unittest.TestCase):
    '''
    Tests for Rating
    '''
    def setUp(self):
        self.client = Client()

    def test_list_rating(self):
        url = reverse('tnd_api_rating_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_rating(self):
        url = reverse('tnd_api_rating_create')
        data = {
            "name": "name",
            "rating_val": "rating_val",
            "adjective": "adjective",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_rating(self):
        rating = create_rating()
        url = reverse('tnd_api_rating_detail', args=[rating.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_rating(self):
        rating = create_rating()
        data = {
            "name": "name",
            "rating_val": "rating_val",
            "adjective": "adjective",
        }
        url = reverse('tnd_api_rating_update', args=[rating.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class GenreViewTest(unittest.TestCase):
    '''
    Tests for Genre
    '''
    def setUp(self):
        self.client = Client()

    def test_list_genre(self):
        url = reverse('tnd_api_genre_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_genre(self):
        url = reverse('tnd_api_genre_create')
        data = {
            "name": "name",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_genre(self):
        genre = create_genre()
        url = reverse('tnd_api_genre_detail', args=[genre.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_genre(self):
        genre = create_genre()
        data = {
            "name": "name",
        }
        url = reverse('tnd_api_genre_update', args=[genre.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


