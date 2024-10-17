import requests

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Book, Rental
from .serializers import BookSerializer, RentalSerializer
from .filters import BookFilter, RentalFilter 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    ordering_fields = ['title', 'author', 'page_count'] 

    @extend_schema(
        parameters=[
            OpenApiParameter(name='title', description='Book title to search', required=True, type=str)
        ]
    )
    @action(detail=False, methods=['get'], url_path='search')  
    def search_books(self, request, *args, **kwargs):
        """Search for books using Google Books API based on the title."""
        title = request.query_params.get('title')
        if not title:
            return Response({"error": "Title parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Google Books API URL
        url = f"https://www.googleapis.com/books/v1/volumes?q={title}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            # Extract relevant book details from Google Books API response
            books = []
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                books.append({
                    "title": volume_info.get('title'),
                    "author": ', '.join(volume_info.get('authors', ['Unknown Author'])),
                    "page_count": volume_info.get('pageCount', 0),
                    "id": item.get('id'),  # Google Books ID
                })

            return Response(books, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    filterset_class = RentalFilter  
    ordering_fields = ['rental_date', 'return_date', 'student__username'] 

    def create(self, request, *args, **kwargs):
        # Ensure book availability and create a new rental
        book_id = request.data.get('book')
        book = Book.objects.get(id=book_id)
        if not book.is_available:
            return Response({"error": "This book is currently unavailable for rental."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Handle return of the book and mark it as available
        rental = self.get_object()
        if 'return_date' in request.data:
            rental.return_date = request.data['return_date']
            rental.save()
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Provide detailed rental information, including fees
        rental = self.get_object()
        serializer = self.get_serializer(rental)
        return Response(serializer.data)
