from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'album', api.AlbumViewSet)
router.register(r'artist', api.ArtistViewSet)
router.register(r'rating', api.RatingViewSet)
router.register(r'genre', api.GenreViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Album
    path('tnd_api/album/', views.AlbumListView.as_view(), name='tnd_api_album_list'),
    path('tnd_api/album/create/', views.AlbumCreateView.as_view(), name='tnd_api_album_create'),
    path('tnd_api/album/detail/<slug:slug>/', views.AlbumDetailView.as_view(), name='tnd_api_album_detail'),
    path('tnd_api/album/update/<slug:slug>/', views.AlbumUpdateView.as_view(), name='tnd_api_album_update'),
)

urlpatterns += (
    # urls for Artist
    path('tnd_api/artist/', views.ArtistListView.as_view(), name='tnd_api_artist_list'),
    path('tnd_api/artist/create/', views.ArtistCreateView.as_view(), name='tnd_api_artist_create'),
    path('tnd_api/artist/detail/<slug:slug>/', views.ArtistDetailView.as_view(), name='tnd_api_artist_detail'),
    path('tnd_api/artist/update/<slug:slug>/', views.ArtistUpdateView.as_view(), name='tnd_api_artist_update'),
)

urlpatterns += (
    # urls for Rating
    path('tnd_api/rating/', views.RatingListView.as_view(), name='tnd_api_rating_list'),
    path('tnd_api/rating/create/', views.RatingCreateView.as_view(), name='tnd_api_rating_create'),
    path('tnd_api/rating/detail/<slug:slug>/', views.RatingDetailView.as_view(), name='tnd_api_rating_detail'),
    path('tnd_api/rating/update/<slug:slug>/', views.RatingUpdateView.as_view(), name='tnd_api_rating_update'),
)

urlpatterns += (
    # urls for Genre
    path('tnd_api/genre/', views.GenreListView.as_view(), name='tnd_api_genre_list'),
    path('tnd_api/genre/create/', views.GenreCreateView.as_view(), name='tnd_api_genre_create'),
    path('tnd_api/genre/detail/<slug:slug>/', views.GenreDetailView.as_view(), name='tnd_api_genre_detail'),
    path('tnd_api/genre/update/<slug:slug>/', views.GenreUpdateView.as_view(), name='tnd_api_genre_update'),
)

