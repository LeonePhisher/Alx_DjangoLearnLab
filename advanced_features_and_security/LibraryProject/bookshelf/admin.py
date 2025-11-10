# LibraryProject/bookshelf/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Book, BorrowRecord

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model."""
    
    model = CustomUser
    
    # Fields to display in the user list
    list_display = (
        'email', 
        'first_name', 
        'last_name', 
        'date_of_birth',
        'is_staff',
        'is_active'
    )
    
    # Fields for searching users
    search_fields = ('email', 'first_name', 'last_name')
    
    # Default ordering
    ordering = ('email',)
    
    # Fieldsets for the edit user page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 
                'last_name', 
                'date_of_birth', 
                'profile_photo'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': (
                'last_login', 
                'date_joined'
            )
        }),
    )
    
    # Fieldsets for the add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'password1', 
                'password2',
                'first_name',
                'last_name',
                'date_of_birth',
                'profile_photo'
            ),
        }),
    )
    
    # Filter options
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

# Register the models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)
admin.site.register(BorrowRecord)