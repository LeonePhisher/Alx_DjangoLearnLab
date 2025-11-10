# Add this import at the top
from .forms import ExampleForm

# Add this view function to the views.py file
@login_required
def example_form_view(request):
    """
    Example view demonstrating secure form handling with ExampleForm.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Security: Process cleaned and validated data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Security: Log the form submission
            logger.info(f"Example form submitted by {name} ({email})")
            
            # In a real application, you might save to database or send email
            messages.success(request, 'Thank you for your submission!')
            return redirect('example_form_success')
        else:
            # Security: Log form validation errors
            logger.warning(f"Example form validation failed: {form.errors}")
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})


@login_required
def example_form_success(request):
    """Success page for example form submission."""
    return render(request, 'bookshelf/example_form_success.html')
