from rest_framework import serializers
from .models import Book, Rental

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'page_count', 'is_available']

class RentalSerializer(serializers.ModelSerializer):
    rental_fee = serializers.ReadOnlyField()  # Include the calculated fee in the response
    is_free_period = serializers.ReadOnlyField()  # Indicate if it's still within the free period

    class Meta:
        model = Rental
        fields = ['id', 'book', 'student', 'rental_date', 'return_date', 'rental_fee', 'is_free_period']

    def create(self, validated_data):
        """Handle availability of books and create a new rental"""
        book = validated_data['book']
        if not book.is_available:
            raise serializers.ValidationError("This book is currently not available for rental.")
        return super().create(validated_data)
