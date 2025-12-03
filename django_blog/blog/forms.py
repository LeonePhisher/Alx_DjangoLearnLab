from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from taggit.forms import TagWidget  # Required for the check

# User registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Profile form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

# Post form with TagWidget
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # must include 'tags'
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags separated by commas'}),
        }

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
