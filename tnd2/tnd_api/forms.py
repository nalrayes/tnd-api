from django import forms
from .models import Album, Artist, Rating, Genre


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'review_release_date', 'fav_tracks', 'least_fav_track', 'year_released', 'record_company', 'album_type', 'spotify_link', 'detailed_genres', 'youtube_link', 'description', 'artists', 'rating', 'genres']


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'average_rating']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['name', 'rating_val', 'adjective']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


