import operator
import functools
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Album, Artist, Rating, Genre
from .forms import AlbumForm, ArtistForm, RatingForm, GenreForm
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

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

def _create_next_page_url_to_format(request):
    request_url =request.build_absolute_uri()
    if "page" in request.GET:
        before_page, after_page = request_url.split("page=")
        before_page += "page="
        after_page = after_page.lstrip('123456789')
        return before_page + "%d" + after_page
    elif len(request.GET) > 1:
        return request_url + "&page=%d"
    else:
        return request_url + "?page=%d"

def albums(request):
    params = request.GET.copy()
    max = 50
    format_for_page = _create_next_page_url_to_format(request)
    if "max" in params:
        max = int(params.pop("max")[0])
    sort_by = "review_release_date"
    if "sort-by" in params:
        sort_by = params.pop("sort-by")[0]
        if sort_by == "rating":
            sort_by = "-rating__rating_val"
    page = 1
    if "page" in params:
        page = int(params.pop("page")[0])
    albums_obj = {"status": "success", "albums": [], "meta": {}}
    if len(params) > 0:
        all_albums = _get_albums_with_params(params)
    else:
        all_albums = Album.objects.all()

    all_albums = all_albums.order_by(sort_by)
    all_albums_paginator = Paginator(all_albums, max)

    albums_page = all_albums_paginator.get_page(page)
    for a in albums_page:
        albums_obj["albums"].append(_create_album_json(a))
    albums_obj["numResults"] = len(all_albums)
    if albums_page.has_next():
        next_page_num = albums_page.next_page_number()
        albums_obj["meta"]["nextPage"] = next_page_num
        albums_obj["meta"]["nextPageURL"] = format_for_page % next_page_num

    if albums_page.has_previous():
        prev_page_num = albums_page.previous_page_number()
        albums_obj["meta"]["prevPage"] = prev_page_num
        albums_obj["meta"]["prevPageURL"] = format_for_page % prev_page_num
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
