import django_filters
from .models import Movie, Genre, Director
from datetime import date

class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label="Title"
    )
    
    genre = django_filters.ModelChoiceFilter(
        field_name='genres', 
        queryset=Genre.objects.all(), 
        label="Genre",
        empty_label="-- all genres --"
    )
    
    director = django_filters.ModelChoiceFilter(
        field_name='director', 
        queryset=Director.objects.all(), 
        label="Director",
        empty_label="-- all directors --"
    )
    
    year = django_filters.ChoiceFilter(
        method='filter_by_decade', 
        label="Decade",
        empty_label=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        current_year = date.today().year
        decades = [(str(y), f"{y}s") for y in range(1900, current_year + 1, 10)]

        # most recent decade first
        self.filters['year'].extra['choices'] = [('', '-- all years --')] + decades[::-1]

    def filter_by_decade(self, queryset, name, value):
        if value:
            year_int = int(value)
            return queryset.filter(
                release_date__year__gte=year_int, 
                release_date__year__lte=year_int + 9
            )
        return queryset

    class Meta:
        model = Movie
        fields = []