from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (list_books, LibraryDetailView, register, 
                   admin_view, librarian_view, member_view,
                   add_book, edit_book, delete_book,
                   add_book/, edit_book/,
                   BookCreateView, BookUpdateView, BookDeleteView)
from django.contrib.auth.decorators import login_required

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),
    
    # Protected views - require login
    path('books/', login_required(list_books), name='list_books'),
    path('library/<int:pk>/', login_required(LibraryDetailView.as_view()), name='library_detail'),
    
    # Role-based views
    path('admin/dashboard/', admin_view, name='admin_view'),
    path('librarian/dashboard/', librarian_view, name='librarian_view'),
    path('member/dashboard/', member_view, name='member_view'),
    
    # Permission-based book views (function-based)
    path('books/add/', add_book, name='add_book'),
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),
    
    # Alternative: Class-based permission views
    # path('books/add/', BookCreateView.as_view(), name='add_book'),
    # path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='edit_book'),
    # path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='delete_book'),
]


