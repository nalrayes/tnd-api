import operator
import functools
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Album, Artist, Rating, Genre
from .forms import AlbumForm, ArtistForm, RatingForm, GenreForm
from django.http import JsonResponse
from django.db.models import Q

def _create_album_json(album):
    res = {
        'id': album.id,
        'title': album.title,
        'fav-tracks': album.fav_tracks,
        'least-fav-track': album.least_fav_track,
        'year': album.year_released,
        'record-company': album.record_company,
        'type': album.album_type,
        'detailed-genres': album.detailed_genres,
        'youtube-link': album.youtube_link,
        'rating': album.rating.rating_val,
        }
    artist_list = []
    for artist in album.artists.all():
        artist_list.append({"id": artist.id, "name": artist.name})
    res["artists"] = artist_list
    return res

def _get_albums_with_params(params):
    query_objects = []
    if "genres" in params:
        for genre in params["genres"].split(","):
            query_objects.append(Q(detailed_genres__contains=genre))
    return Album.objects.filter(functools.reduce(operator.and_, query_objects))

def albums(request):
    params = request.GET.copy()
    max = 50
    if "max" in params:
        max = int(params.pop("max")[0])
    sort_by = "review_release_date"
    if "sort-by" in params:
        sort_by = params.pop("sort-by")[0]
        if sort_by == "rating":
            sort_by = "-rating__rating_val"
    albums_obj = {"status": "success", "albums": []}
    if len(params) > 0:
        all_albums = _get_albums_with_params(params)
    else:
        all_albums = Album.objects.all()

    all_albums = all_albums.order_by(sort_by)[:max]

    for a in all_albums:
        albums_obj["albums"].append(_create_album_json(a))
    return JsonResponse(albums_obj)
def _create_min_album_json(album):
    res = {
        "id": album.id,
        "title": album.title,
        "detailed-genres": album.detailed_genres,
        'youtube-link': album.youtube_link,
        "rating": album.rating.rating_val,
    }
    return res

def _create_artist_json(artist):
    res = {
        "id": artist.id,
        "name": artist.name,
        "albums": [],
    }

    albums = artist.album_set.all()
    for a in albums:
        res['albums'].append(_create_min_album_json(a))
    return res

def artists(request):
    params = request.GET.copy()
    max = 50
    if "max" in params:
        max = int(params.pop("max")[0])
    all_artists = Artist.objects.all()
    artists_obj = {"status": "success", "artists": []}
    for a in all_artists:
        if a.album_set.count() > 1:
            artists_obj["artists"].append(_create_artist_json(a))
    return JsonResponse(artists_obj)
