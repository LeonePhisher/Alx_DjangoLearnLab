from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


# ----------------------------------------------------------
# LIST VIEW (GET all books)
# Anyone can read books (Read-only for unauthenticated users)
# ----------------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ----------------------------------------------------------
# DETAIL VIEW (GET one book)
# Also read-only for unauthenticated users
# ----------------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "pk"


# ----------------------------------------------------------
# CREATE VIEW (POST)
# Only authenticated users can create books
# ----------------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# ----------------------------------------------------------
# UPDATE VIEW (PUT/PATCH)
# Only authenticated users can update books
# ----------------------------------------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()


# ----------------------------------------------------------
# DELETE VIEW (DELETE)
# Only authenticated users can delete books
# ----------------------------------------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
