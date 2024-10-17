from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RentalViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
