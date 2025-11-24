from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        
        # Create Authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")
        
        # Create Books
        self.book1 = Book.objects.create(title="Book One", publication_year=2020, author=self.author1)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2021, author=self.author2)

    # -----------------------------
    # Helper function to login
    # -----------------------------
    def authenticate(self):
        self.client.login(username='testuser', password='testpass')

    # -----------------------------
    # Test: List all books
    # -----------------------------
    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # -----------------------------
    # Test: Retrieve single book
    # -----------------------------
    def test_retrieve_book(self):
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # -----------------------------
    # Test: Create book (authenticated)
    # -----------------------------
    def test_create_book_authenticated(self):
        self.authenticate()
        data = {
            "title": "Book Three",
            "publication_year": 2022,
            "author": self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "Book Three")

    # -----------------------------
    # Test: Create book (unauthenticated)
    # -----------------------------
    def test_create_book_unauthenticated(self):
        data = {
            "title": "Book Four",
            "publication_year": 2022,
            "author": self.author2.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------
    # Test: Update book
    # -----------------------------
    def test_update_book(self):
        self.authenticate()
        data = {
            "title": "Updated Book One",
            "publication_year": 2021,
            "author": self.author1.id
        }
        response = self.client.put(f'/api/books/update/{self.book1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book One")

    # -----------------------------
    # Test: Delete book
    # -----------------------------
    def test_delete_book(self):
        self.authenticate()
        response = self.client.delete(f'/api/books/delete/{self.book2.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # -----------------------------
    # Test: Filtering
    # -----------------------------
    def test_filter_books_by_title(self):
        response = self.client.get('/api/books/?title=Book One')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book One")

    # -----------------------------
    # Test: Searching
    # -----------------------------
    def test_search_books_by_author_name(self):
        response = self.client.get('/api/books/?search=Author Two')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author2.id)

    # -----------------------------
    # Test: Ordering
    # -----------------------------
    def test_order_books_by_publication_year_desc(self):
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
