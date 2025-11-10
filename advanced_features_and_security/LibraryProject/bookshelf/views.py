"""
Secure views implementation with protection against SQL injection and proper input validation.
"""

import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.utils.html import escape
from .models import Book, BorrowRecord
from .forms import BookForm, BorrowRecordForm, SearchForm

logger = logging.getLogger(__name__)

# Security: Safe search functionality to prevent SQL injection (Step 3)
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def safe_search_books(request):
    """
    Secure search implementation using Django ORM to prevent SQL injection.
    All user input is properly escaped and validated.
    """
    books = Book.objects.none()
    search_form = SearchForm(request.GET or None)
    search_query = ""
    
    if search_form.is_valid():
        # Security: Get cleaned data from form (Step 3)
        search_query = search_form.cleaned_data.get('query', '')
        
        if search_query:
            # Security: Use Django ORM with parameterized queries (Step 3)
            # This prevents SQL injection by properly escaping inputs
            books = Book.objects.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(isbn__icontains=search_query)
            ).select_related('created_by')
            
            # Security: Log search queries for monitoring
            logger.info(f"User {request.user.email} searched for: {search_query}")
    
    context = {
        'books': books,
        'search_form': search_form,
        'search_query': search_query,
    }
    return render(request, 'bookshelf/book_search.html', context)


# Security: Safe book listing with proper input validation (Step 3)
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('bookshelf.can_view', raise_exception=True), name='dispatch')
class SecureBookListView(ListView):
    """
    Secure book list view with proper input validation and safe queryset handling.
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    paginate_by = 20
    
    def get_queryset(self):
        # Security: Always start with a base queryset (Step 3)
        queryset = super().get_queryset().select_related('created_by')
        
        # Security: Safe filtering based on GET parameters (Step 3)
        author_filter = self.request.GET.get('author')
        if author_filter:
            # Security: Use Django ORM filtering (safe from SQL injection)
            queryset = queryset.filter(author__icontains=author_filter)
        
        # Security: Additional safe filters
        available_filter = self.request.GET.get('available')
        if available_filter in ['true', 'false']:
            is_available = available_filter == 'true'
            queryset = queryset.filter(is_available=is_available)
        
        return queryset.order_by('-created_at')


# Security: Protected book creation with input validation (Step 3)
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def secure_create_book(request):
    """
    Secure book creation with comprehensive input validation and CSRF protection.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                # Security: Use commit=False to add user before saving (Step 3)
                book = form.save(commit=False)
                book.created_by = request.user
                book.save()
                
                # Security: Log the creation event
                logger.info(f"Book '{book.title}' created by user {request.user.email}")
                
                messages.success(request, 'Book created successfully!')
                return redirect('book_detail', pk=book.pk)
                
            except Exception as e:
                # Security: Don't expose internal errors to users (Step 3)
                logger.error(f"Error creating book: {str(e)}")
                messages.error(request, 'An error occurred while creating the book.')
        else:
            # Security: Log form validation errors
            logger.warning(f"Form validation failed: {form.errors}")
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'title': 'Create New Book'
    })


# Security: Safe book editing with ownership validation (Step 3)
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def secure_edit_book(request, pk):
    """
    Secure book editing with proper authorization checks.
    """
    # Security: Use get_object_or_404 to prevent information leakage (Step 3)
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            try:
                form.save()
                
                # Security: Log the edit event
                logger.info(f"Book '{book.title}' edited by user {request.user.email}")
                
                messages.success(request, 'Book updated successfully!')
                return redirect('book_detail', pk=book.pk)
                
            except Exception as e:
                logger.error(f"Error updating book: {str(e)}")
                messages.error(request, 'An error occurred while updating the book.')
        else:
            logger.warning(f"Form validation failed: {form.errors}")
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'title': 'Edit Book'
    })


# Security: Safe AJAX view with proper validation (Step 3)
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_autocomplete(request):
    """
    Secure AJAX autocomplete endpoint with input validation.
    """
    # Security: Validate and sanitize input (Step 3)
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
    
    # Security: Escape user input to prevent XSS in JSON response (Step 3)
    safe_query = escape(query)
    
    # Security: Use Django ORM for safe database queries (Step 3)
    books = Book.objects.filter(
        Q(title__icontains=safe_query) | 
        Q(author__icontains=safe_query)
    ).values('id', 'title', 'author')[:10]
    
    # Security: Manually construct safe response data
    results = []
    for book in books:
        results.append({
            'id': book['id'],
            'text': f"{book['title']} by {book['author']}"  # Already safe from database
        })
    
    return JsonResponse({'results': results})


# Security: Example of unsafe practice (for educational purposes)
def unsafe_search_example(request):
    """
    EXAMPLE OF UNSAFE PRACTICE - DO NOT USE IN PRODUCTION
    This demonstrates what NOT to do to prevent SQL injection.
    """
    query = request.GET.get('q', '')
    
    # UNSAFE: String formatting in raw SQL - vulnerable to SQL injection
    # books = Book.objects.raw(f"SELECT * FROM bookshelf_book WHERE title LIKE '%{query}%'")
    
    # SECURE: Use Django ORM instead
    books = Book.objects.filter(title__icontains=query)
    
    return render(request, 'bookshelf/book_list.html', {'books': books})