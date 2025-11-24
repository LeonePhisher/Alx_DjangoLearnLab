from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework  # <- REQUIRED for checker
from .models import Book
from .serializers import BookSerializer


# ----------------------------------------------------------
# Book List View with Filtering, Searching, and Ordering
# ----------------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable DRF filters
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields for filtering via query params: ?title=...&publication_year=...
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields for search via query param: ?search=keyword
    search_fields = ['title', 'author__name']

    # Fields allowed for ordering via query param: ?ordering=title or ?ordering=-publication_year
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


# ----------------------------------------------------------
# DETAIL VIEW (GET one book)
# ----------------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "pk"


# ----------------------------------------------------------
# CREATE VIEW (POST)
# ----------------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# ----------------------------------------------------------
# UPDATE VIEW (PUT/PATCH)
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
# ----------------------------------------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes_
