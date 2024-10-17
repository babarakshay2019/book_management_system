import django_filters
from .models import Book, Rental

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')  # Case-insensitive partial match
    author = django_filters.CharFilter(lookup_expr='icontains')
    is_available = django_filters.BooleanFilter()

    class Meta:
        model = Book
        fields = ['title', 'author', 'is_available']


class RentalFilter(django_filters.FilterSet):
    book_title = django_filters.CharFilter(field_name='book__title', lookup_expr='icontains')
    student_name = django_filters.CharFilter(field_name='student__username', lookup_expr='icontains')
    rental_date = django_filters.DateFilter()
    return_date = django_filters.DateFilter()

    class Meta:
        model = Rental
        fields = ['book_title', 'student_name', 'rental_date', 'return_date']