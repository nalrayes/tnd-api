from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import *
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields


class Artist(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    average_rating = models.DecimalField(max_digits=5, decimal_places=2)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('tnd_api_artist_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('tnd_api_artist_update', args=(self.slug,))


class Rating(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    rating_val = models.IntegerField()
    adjective = models.CharField(max_length=30)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('tnd_api_rating_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('tnd_api_rating_update', args=(self.slug,))


class Genre(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('tnd_api_genre_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('tnd_api_genre_update', args=(self.slug,))
        
class Album(models.Model):

    # Fields
    title = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    review_release_date = models.DateField()
    fav_tracks = models.TextField(max_length=510)
    least_fav_track = models.CharField(max_length=100)
    year_released = models.IntegerField()
    record_company = models.CharField(max_length=100)
    album_type = models.CharField(max_length=30)
    spotify_link = models.URLField()
    detailed_genres = models.CharField(max_length=100)
    youtube_link = models.URLField()
    description = models.TextField(max_length=500)

    # Relationship Fields
    artists = models.ManyToManyField(Artist)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('tnd_api_albums_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('tnd_api_albums_update', args=(self.slug,))
