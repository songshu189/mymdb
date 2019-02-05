from django.views.generic import (
    ListView, DetailView,
)

from core.models import Movie


class MovieDetail(DetailView):
    model = Movie

class MovieList(ListView):
    model = Movie
    paginate_by = 10
