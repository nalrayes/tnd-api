from . import models
from . import serializers
from rest_framework import viewsets, permissions


class AlbumViewSet(viewsets.ModelViewSet):
    """ViewSet for the Album class"""

    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArtistViewSet(viewsets.ModelViewSet):
    """ViewSet for the Artist class"""

    queryset = models.Artist.objects.all()
    serializer_class = serializers.ArtistSerializer
    permission_classes = [permissions.IsAuthenticated]


class RatingViewSet(viewsets.ModelViewSet):
    """ViewSet for the Rating class"""

    queryset = models.Rating.objects.all()
    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.IsAuthenticated]


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet for the Genre class"""

    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAuthenticated]


