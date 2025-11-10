"""
Secure forms with input validation and sanitization.
Includes ExampleForm as required.
"""

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Book, BorrowRecord

class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form practices with various field types.
    This form showcases proper input validation and security measures.
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        }),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z\s\-\.]+$',
                message='Name can only contain letters, spaces, hyphens, and periods.'
            )
        ]
    )
    
    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'maxlength': '500'  # Security: Limit input size
        }),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9\s\-\.\,\!\?\(\)\:\;\'\"]+$',
                message='Message contains invalid characters.'
            )
        ]
    )
    
    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=150,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        })
    )
    
    agree_to_terms = forms.BooleanField(
        required=True,
        label='I agree to the terms and conditions'
    )
    
    def clean_name(self):
        """Security: Additional name validation"""
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long.")
        
        # Security: Check for potentially malicious patterns
        suspicious_patterns = ['<script>', 'javascript:', 'onload=', 'onerror=']
        for pattern in suspicious_patterns:
            if pattern in name.lower():
                raise ValidationError("Invalid characters in name.")
        
        return name
    
    def clean_message(self):
        """Security: Message content validation"""
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        
        # Security: Prevent excessively long words (potential DoS)
        words = message.split()
        for word in words:
            if len(word) > 50:
                raise ValidationError("Message contains words that are too long.")
        
        return message
    
    def clean(self):
        """Security: Cross-field validation"""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        age = cleaned_data.get('age')
        
        # Example of cross-field validation
        if age and age < 18 and name:
            # Security: Log potential underage submissions
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Underage form submission from: {name}")
        
        return cleaned_data


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
