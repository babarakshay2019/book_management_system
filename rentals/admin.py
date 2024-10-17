from django.contrib import admin
from .models import Book, Rental

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'page_count', 'is_available')
    search_fields = ('title', 'author')  # Enable searching by title and author
    list_filter = ('is_available',)  # Filter books based on availability

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'rental_date', 'return_date')
    search_fields = ('book__title', 'student__email')  # Search by book title and student email
    list_filter = ('rental_date', 'return_date')  # Filter by rental and return date
