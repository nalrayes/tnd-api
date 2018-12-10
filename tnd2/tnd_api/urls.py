from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

# router = routers.DefaultRouter()
# router.register(r'album', api.AlbumViewSet)
# router.register(r'artist', api.ArtistViewSet)
# router.register(r'rating', api.RatingViewSet)
# router.register(r'genre', api.GenreViewSet)


# urlpatterns = (
#     # urls for Django Rest Framework API
#     path('api/v1/', include(router.urls)),
# )

urlpatterns = (
    # urls for Album
    path('albums', views.albums, name='tnd_api_album_list'),
    # path('tnd_api/albums/<slug:slug>/', views.AlbumDetailView.as_view(), name='tnd_api_album_slug'),
    # path('tnd_api/albums/<id:id>/', views.AlbumUpdateView.as_view(), name='tnd_api_album_id'),
)

# urlpatterns += (
#     # urls for Artist
#     path('tnd_api/artists/', views.ArtistListView.as_view(), name='tnd_api_artist_list'),
#     path('tnd_api/artists/<slug:slug>/', views.ArtistCreateView.as_view(), name='tnd_api_artist_slug'),
#     path('tnd_api/artists/<slug:slug>/', views.ArtistCreateView.as_view(), name='tnd_api_artist_slug'),
# )
