from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields for filtering via query params: ?title=...&publication_year=...
    filterset_fields = ['title', 'author', 'publication_year']

    # Fields for search via query param: ?search=keyword
    search_fields = ['title', 'author__name']

    # Fields allowed for ordering via query param: ?ordering=title or ?ordering=-publication_year
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering
