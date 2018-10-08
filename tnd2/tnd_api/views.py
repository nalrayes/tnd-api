from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Album, Artist, Rating, Genre
from .forms import AlbumForm, ArtistForm, RatingForm, GenreForm


class AlbumListView(ListView):
    model = Album


class AlbumCreateView(CreateView):
    model = Album
    form_class = AlbumForm


class AlbumDetailView(DetailView):
    model = Album


class AlbumUpdateView(UpdateView):
    model = Album
    form_class = AlbumForm


class ArtistListView(ListView):
    model = Artist


class ArtistCreateView(CreateView):
    model = Artist
    form_class = ArtistForm


class ArtistDetailView(DetailView):
    model = Artist


class ArtistUpdateView(UpdateView):
    model = Artist
    form_class = ArtistForm


class RatingListView(ListView):
    model = Rating


class RatingCreateView(CreateView):
    model = Rating
    form_class = RatingForm


class RatingDetailView(DetailView):
    model = Rating


class RatingUpdateView(UpdateView):
    model = Rating
    form_class = RatingForm


class GenreListView(ListView):
    model = Genre


class GenreCreateView(CreateView):
    model = Genre
    form_class = GenreForm


class GenreDetailView(DetailView):
    model = Genre


class GenreUpdateView(UpdateView):
    model = Genre
    form_class = GenreForm

