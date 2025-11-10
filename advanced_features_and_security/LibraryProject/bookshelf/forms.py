"""
Secure forms with input validation and sanitization.
"""

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Book, BorrowRecord

class BookForm(forms.ModelForm):
    """
    Secure book form with additional validation.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date', 'description']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_title(self):
        """Security: Validate and sanitize title input"""
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 2:
            raise ValidationError("Title must be at least 2 characters long.")
        return title
    
    def clean_isbn(self):
        """Security: Validate ISBN format"""
        isbn = self.cleaned_data.get('isbn', '').strip()
        if not isbn.replace('-', '').replace(' ', '').isdigit():
            raise ValidationError("ISBN must contain only numbers and hyphens.")
        return isbn


class SearchForm(forms.Form):
    """
    Secure search form with input validation.
    """
    query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search books...'}),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9\s\-\.\',!?]+$',
                message='Search query contains invalid characters.'
            )
        ]
    )
    
    def clean_query(self):
        """Security: Additional search query sanitization"""
        query = self.cleaned_data.get('query', '').strip()
        if len(query) < 2:
            raise ValidationError("Search query must be at least 2 characters long.")
        return query


class BorrowRecordForm(forms.ModelForm):
    """
    Secure borrow record form with validation.
    """
    class Meta:
        model = BorrowRecord
        fields = ['book', 'user', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Security: Only show available books
        self.fields['book'].queryset = Book.objects.filter(is_available=True)