from . import models

from rest_framework import serializers


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Album
        fields = (
            'slug',
            'title',
            'created',
            'last_updated',
            'review_release_date',
            'fav_tracks',
            'least_fav_track',
            'year_released',
            'record_company',
            'album_type',
            'spotify_link',
            'detailed_genres',
            'youtube_link',
            'description',
        )


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Artist
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
        )


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Rating
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
            'rating_val',
            'adjective',
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Genre
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
        )
