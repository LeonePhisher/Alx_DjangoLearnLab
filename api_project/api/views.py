# api/views.py
from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed (read-only).
    Publicly accessible for listing books, but requires authentication for modifications.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow anyone to view the book list

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    Provides all CRUD operations: list, create, retrieve, update, destroy.
    Requires authentication for all operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Allow any user to view books (list and retrieve)
            permission_classes = [AllowAny]
        else:
            # Require authentication for create, update, delete
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
