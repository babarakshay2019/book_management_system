from django.db import models
from datetime import timedelta, date
from django.conf import settings  # Assuming `CustomUser` is the user model

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    page_count = models.IntegerField()
    is_available = models.BooleanField(default=True)  # Indicates if the book is available for rental
    
    def __str__(self):
        return self.title

class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # CustomUser as the user model
    rental_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    
    @property
    def is_free_period(self):
        """ Check if the rental is still within the free 1-month period """
        return date.today() <= self.rental_date + timedelta(days=30)

    @property
    def rental_fee(self):
        """ Calculate fee based on the rental period and book page count """
        if self.is_free_period:
            return 0  # No fee for the first month
        # Calculate the fee after the free period (page count / 100 per month after first month)
        months_extended = (date.today() - (self.rental_date + timedelta(days=30))).days // 30
        return (self.book.page_count / 100) * months_extended

    def save(self, *args, **kwargs):
        # Ensure that when the book is rented, it becomes unavailable
        if not self.return_date:
            self.book.is_available = False  # Mark the book as unavailable when rented
        else:
            self.book.is_available = True  # Mark the book as available when returned
        self.book.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} rented {self.book.title}"
