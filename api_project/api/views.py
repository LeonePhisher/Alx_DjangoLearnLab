# api/views.py
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer