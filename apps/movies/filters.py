import django_filters
from .models import Movie, Genre, Director
from datetime import date

class MovieFilter(django_filters.FilterSet):
    # Filtri basati su relazioni (tendine automatiche)
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
    
    # Filtro per anno trasformato in tendina di decenni
    year = django_filters.ChoiceFilter(
        method='filter_by_decade', 
        label="Decade",
        empty_label=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generiamo le scelte per la tendina: (valore_url, testo_visualizzato)
        current_year = date.today().year
        # range(partenza, stop, step) -> dal 1900 a oggi saltando di 10
        decades = [(str(y), f"{y}s") for y in range(1900, current_year + 1, 10)]
        self.filters['year'].extra['choices'] = [('', '-- all years --')] + decades[::-1] # [::-1] per i più recenti in alto

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
        fields = [] # Lasciamo vuoto perché abbiamo definito tutto sopra