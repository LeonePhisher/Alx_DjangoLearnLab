from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# ----------------------------------------------------------
# LIST VIEW (GET all books)
# Anyone can view books (Read-only access for unauthenticated users)
# ----------------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # public read access


# ----------------------------------------------------------
# DETAIL VIEW (GET one book by ID)
# Also public read access
# ----------------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"   # retrieve by id


# ----------------------------------------------------------
# CREATE VIEW (POST — add a new book)
# Only authenticated users can create a book
# ----------------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Optional hook to customize saving behavior
    def perform_create(self, serializer):
        # We can add extra logic here
        # Example: attach logged-in user automatically (if model had user)
        serializer.save()


# ----------------------------------------------------------
# UPDATE VIEW (PUT/PATCH — edit a book)
# Only authenticated users can update books
# ----------------------------------------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()


# ----------------------------------------------------------
# DELETE VIEW (DELETE — remove a book)
# Only authenticated users can delete books
# ----------------------------------------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"
