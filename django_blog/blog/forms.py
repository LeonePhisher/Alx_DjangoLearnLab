from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

class PostForm(forms.ModelForm):
    tags_field = forms.CharField(required=False, help_text='Comma-separated tags', max_length=200)

    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        # Accept an instance for editing scenario
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['tags_field'] = ', '.join([t.name for t in self.instance.tags.all()])

    def save(self, commit=True, author=None):
        post = super().save(commit=False)
        if author:
            post.author = author
        if commit:
            post.save()
            tags_csv = self.cleaned_data.get('tags_field', '')
            tag_names = [t.strip() for t in tags_csv.split(',') if t.strip()]
            # assign tags
            from .models import Tag
            post.tags.clear()
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name__iexact = name, defaults={'name': name})
                # if the get_or_create above used name__iexact it may error on some DBs; use:
                # tag_obj, _ = Tag.objects.get_or_create(name=name)
                post.tags.add(tag_obj)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
