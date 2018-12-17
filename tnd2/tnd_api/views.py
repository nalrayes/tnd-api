import operator
import functools
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Album, Artist, Rating, Genre
from .forms import AlbumForm, ArtistForm, RatingForm, GenreForm
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator

def _create_artist_link(artist, request):
    return '{}://{}'.format(request.scheme, request.get_host()) + "/tnd_api/artists/" + str(artist.id)

def _create_album_link(album, request):
    return '{}://{}'.format(request.scheme, request.get_host()) + "/tnd_api/albums/" + str(album.id)

def _create_album_json(album, request, include_desc=False, include_artists=True):
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
        'slug': album.slug
        }
    if include_desc:
        res["description"] = album.description
    if include_artists:
        artist_list = []
        for artist in album.artists.all():
            link = _create_artist_link(artist, request)
            artist_list.append({"id": artist.id, "name": artist.name, "slug": artist.slug, "link": link})
        res["artists"] = artist_list
    return res

def _get_albums_with_params(params):
    query_objects = []
    if "genres" in params:
        for genre in params["genres"].split(","):
            query_objects.append(Q(detailed_genres__contains=genre))
    if "title-contains" in params:
        query_objects.append(Q(title__contains=params['title-contains']))
    if "record-company-contains" in params:
        query_objects.append(Q(record_company__contains=params['record-company-contains']))
    if "artist-contains" in params:
        query_objects.append(Q(artists__name__contains=params["artist-contains"]))
    if "rating-exact" in params:
        int_rating = int(params["rating-exact"])
        query_objects.append(Q(rating__rating_val=int_rating))
    if "rating-less-than" in params:
        int_rating = int(params["rating-less-than"])
        query_objects.append(Q(rating__rating_val__lte=int_rating))
    if "rating-greater-than" in params:
        int_rating = int(params["rating-greater-than"])
        query_objects.append(Q(rating__rating_val__gte=int_rating))
    if "album-released-year" in params:
        int_album_year = int(params["album-released-year"])
        query_objects.append(Q(year_released=int_album_year))
    if "record-company-contains" in params:
        query_objects.append(Q(record_company__contains=params["record-company"]))
    if "album-type" in params:
        query_objects.append(Q(album_type=params["album-type"]))

    return Album.objects.filter(functools.reduce(operator.and_, query_objects))

def _create_next_page_url_to_format(request):
    request_url =request.build_absolute_uri()
    if "page" in request.GET:
        before_page, after_page = request_url.split("page=")
        before_page += "page="
        after_page = after_page.lstrip('123456789')
        return before_page + "%d" + after_page
    elif len(request.GET) > 1:
        return request_url + "&page={}"
    else:
        return request_url + "?page={}"

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
    include_desc = False
    if "include-desc" in params:
        include_desc_str = params.pop("include-desc")[0]
        include_desc = include_desc_str == "true"
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
        albums_obj["albums"].append(_create_album_json(a, request, include_desc=include_desc))
    albums_obj["numResults"] = len(all_albums)
    if albums_page.has_next():
        next_page_num = albums_page.next_page_number()
        albums_obj["meta"]["nextPage"] = next_page_num
        print("hello")
        print(format_for_page, next_page_num)
        albums_obj["meta"]["nextPageURL"] = format_for_page.format(next_page_num)

    if albums_page.has_previous():
        prev_page_num = albums_page.previous_page_number()
        albums_obj["meta"]["prevPage"] = prev_page_num
        albums_obj["meta"]["prevPageURL"] = format_for_page.format(prev_page_num)
    return JsonResponse(albums_obj)

def single_album(request, id):
    album = Album.objects.get(id=id)
    res = {"status": "success"}
    res["album"] = _create_album_json(album, request, include_desc=True)
    return JsonResponse(res)

def single_album_slug(request, slug):
    album = Album.objects.get(slug=slug)
    res = {"status": "success"}
    res["album"] = _create_album_json(album, request, include_desc=True)
    return JsonResponse(res)

def single_artist(request, id):
    artist = Artist.objects.get(id=id)
    res = {"status": "success"}
    res["artist"] = _create_artist_json(artist, request)
    return JsonResponse(res)

def single_artist_slug(request, slug):
    artist = Artist.objects.get(slug=slug)
    res = {"status": "success"}
    res["album"] = _create_artist_json(artist, request)
    return JsonResponse(res)

def _create_min_album_json(album, request):
    res = {
        "id": album.id,
        "title": album.title,
        "detailed-genres": album.detailed_genres,
        'youtube-link': album.youtube_link,
        "rating": album.rating.rating_val,
        "slug": album.slug,
        "link": _create_album_link(album, request),
    }
    return res

def _create_artist_json(artist, request):
    res = {
        "id": artist.id,
        "name": artist.name,
        "slug": artist.slug,
        "albums": [],
    }

    albums = artist.album_set.all()
    for a in albums:
        res['albums'].append(_create_min_album_json(a, request))
    return res
def _get_artists_with_params(params):
    query_objects = []
    artist_objects = Artist.objects
    if "name-contains" in params:
        query_objects.append(Q(name__contains=params["name-contains"]))
    if "genres" in params:
        for genre in params["genres"].split(","):
            query_objects.append(Q(album__detailed_genres__contains=genre))
    if "record-company-contains" in params:
        query_objects.append(Q(album__record_companny__contains=params["record-company-contains"]))
    if "rating-exact" in params:
        int_rating = int(params["rating-exact"])
        query_objects.append(Q(album__rating__rating_val=int_rating))
    if "rating-less-than" in params:
        int_rating = int(params["rating-less-than"])
        query_objects.append(Q(album__rating__rating_val__lte=int_rating))
    if "rating-greater-than" in params:
        int_rating = int(params["rating-greater-than"])
        query_objects.append(Q(album__rating__rating_val__gte=int_rating))
    if "album-count" in params:
        artist_objects = artist_objects.annotate(num_albums=Count('album'))
        int_count = int(params["album-count"])
        query_objects.append(Q(num_albums=int_count))

    return artist_objects.filter(functools.reduce(operator.and_, query_objects))


def artists(request):
    params = request.GET.copy()
    max = 50
    format_for_page = _create_next_page_url_to_format(request)
    if "max" in params:
        max = int(params.pop("max")[0])
    page = 1
    if "page" in params:
        page = int(params.pop("page")[0])

    artists_obj = {"status": "success", "artists": [], "meta": {}}

    if len(params) > 0:
        all_artists = _get_artists_with_params(params)
    else:
        all_artists = Artist.objects.all()
    all_artists_paginator = Paginator(all_artists, max)

    artists_page = all_artists_paginator.get_page(page)
    for a in artists_page:
        artists_obj["artists"].append(_create_artist_json(a, request))
    artists_obj["numResults"] = len(all_artists)
    if artists_page.has_next():
        next_page_num = artists_page.next_page_number()
        artists_obj["meta"]["nextPage"] = next_page_num
        artists_obj["meta"]["nextPageURL"] = format_for_page.format(next_page_num)
    if artists_page.has_previous():
        prev_page_num = artists_page .previous_page_number()
        artists_obj["meta"]["prevPage"] = prev_page_num
        artists_obj["meta"]["prevPageURL"] = format_for_page.format(prev_page_num)
    return JsonResponse(artists_obj)
