from django.contrib import admin
from django import forms
from .models import Album, Artist, Rating, Genre

class AlbumAdminForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = '__all__'


class AlbumAdmin(admin.ModelAdmin):
    form = AlbumAdminForm
    rating_val = lambda album: album.rating.rating_val
    rating_val.short_description = "rating"
    list_display = ['title', 'slug', rating_val, 'created', 'last_updated', 'review_release_date', 'fav_tracks', 'least_fav_track', 'year_released', 'record_company', 'album_type', 'spotify_link', 'detailed_genres', 'youtube_link']
    # readonly_fields = ['title', 'slug', 'created', 'last_updated', 'review_release_date', 'fav_tracks', 'least_fav_track', 'year_released', 'record_company', 'album_type', 'spotify_link', 'detailed_genres', 'youtube_link', 'description']

admin.site.register(Album, AlbumAdmin)


class ArtistAdminForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = '__all__'


class ArtistAdmin(admin.ModelAdmin):
    form = ArtistAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated']
    readonly_fields = ['name', 'slug']

admin.site.register(Artist, ArtistAdmin)


class RatingAdminForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = '__all__'


class RatingAdmin(admin.ModelAdmin):
    form = RatingAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'rating_val', 'adjective']
    readonly_fields = ['name', 'slug', 'created', 'last_updated', 'rating_val', 'adjective']

admin.site.register(Rating, RatingAdmin)


class GenreAdminForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = '__all__'


class GenreAdmin(admin.ModelAdmin):
    form = GenreAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated']
    readonly_fields = ['name', 'slug', 'created', 'last_updated']

admin.site.register(Genre, GenreAdmin)
