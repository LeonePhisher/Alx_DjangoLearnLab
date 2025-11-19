# api/views.py
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Keep the existing BookList view for backward compatibility
class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# New ViewSet for full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    Provides all CRUD operations: list, create, retrieve, update, destroy.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
