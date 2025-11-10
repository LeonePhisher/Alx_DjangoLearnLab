from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Book, Library, UserProfile, Author
from .forms import BookForm
from django.contrib.auth.decorators import permission_required

# Utility function to check user roles
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'

# Function-based view to list all books
@login_required
def list_books(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Role-based views
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    users = User.objects.all().select_related('profile')
    return render(request, 'relationship_app/admin_view.html', {'users': users})

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    books = Book.objects.all().select_related('author')
    libraries = Library.objects.all()
    return render(request, 'relationship_app/librarian_view.html', {
        'books': books,
        'libraries': libraries
    })

@login_required
@user_passes_test(is_member)
def member_view(request):
    user_books = Book.objects.all().select_related('author')[:10]
    return render(request, 'relationship_app/member_view.html', {'books': user_books})

# Permission-based views for Books
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {
        'form': form,
        'title': 'Add New Book'
    })

@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {
        'form': form,
        'title': 'Edit Book'
    })

@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})

# Class-based views with permissions (alternative approach)
class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    permission_required = 'relationship_app.can_add_book'
    success_url = reverse_lazy('relationship_app:list_books')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Book'
        return context

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    permission_required = 'relationship_app.can_change_book'
    success_url = reverse_lazy('relationship_app:list_books')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Book'
        return context

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'relationship_app/book_confirm_delete.html'
    permission_required = 'relationship_app.can_delete_book'
    success_url = reverse_lazy('relationship_app:list_books')

