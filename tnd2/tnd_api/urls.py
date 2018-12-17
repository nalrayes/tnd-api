from django.urls import path, include
from rest_framework import routers

from . import views

urlpatterns = (
    # urls for Album
    path('albums', views.albums, name='tnd_api_album_list'),
    path('albums/<int:id>', views.single_album, name='tnd_api_album_id'),
    path('albums/<slug:slug>', views.single_album_slug, name='tnd_api_album_slug'),
)

urlpatterns += (
    # urls for Artist
    path('artists', views.artists, name='tnd_api_artist_list'),
    path('artists/<int:id>', views.single_artist, name='tnd_api_artist_if'),
    path('artists/<slug:slug>', views.single_artist_slug, name='tnd_api_artist_slug'),
)
