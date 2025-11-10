"""
URL configuration for bookshelf app with secure views.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.SecureBookListView.as_view(), name='book_list'),
    path('search/', views.safe_search_books, name='book_search'),
    path('create/', views.secure_create_book, name='create_book'),
    path('<int:pk>/edit/', views.secure_edit_book, name='edit_book'),
    path('autocomplete/', views.book_autocomplete, name='book_autocomplete'),
    # Example form routes
    path('example-form/', views.example_form_view, name='example_form_view'),
    path('example-form/success/', views.example_form_success, name='example_form_success'),
    # Security: Example of unsafe route (for educational purposes only)
    path('unsafe-search/', views.unsafe_search_example, name='unsafe_search_example'),
]
