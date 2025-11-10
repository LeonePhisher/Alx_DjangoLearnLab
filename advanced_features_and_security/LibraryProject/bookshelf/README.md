# Django Permissions and Groups Implementation

## Overview
This implementation demonstrates Django's permission and group system with custom permissions for a library management application.

## Custom Permissions Defined

### Book Model Permissions
- `can_view` - Permission to view books
- `can_create` - Permission to create new books  
- `can_edit` - Permission to edit existing books
- `can_delete` - Permission to delete books

### BorrowRecord Model Permissions
- `can_view_borrow` - Permission to view borrow records
- `can_create_borrow` - Permission to create borrow records
- `can_edit_borrow` - Permission to edit borrow records
- `can_delete_borrow` - Permission to delete borrow records

## Groups Configuration

### Predefined Groups
1. **Viewers** - Can only view books and borrow records
2. **Editors** - Can view, create, and edit books and borrow records  
3. **Admins** - Has all permissions for complete system access

### Setting Up Groups
Run the management command to create groups with appropriate permissions:
```bash
python manage.py setup_groups
