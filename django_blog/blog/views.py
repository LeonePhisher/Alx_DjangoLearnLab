from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Post, Comment, Tag
from .forms import UserRegisterForm, ProfileForm, PostForm, CommentForm

# AUTH: registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            # create profile data
            profile = user.profile
            profile.bio = profile_form.cleaned_data.get('bio')
            if profile_form.cleaned_data.get('avatar'):
                profile.avatar = profile_form.cleaned_data.get('avatar')
            profile.save()
            login(request, user)
            messages.success(request, 'Your account was created and you are now logged in.')
            return redirect('blog:post-list')
    else:
        form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'blog/register.html', {'form': form, 'profile_form': profile_form})

# PROFILE
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        pform = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if pform.is_valid():
            pform.save()
            messages.success(request, 'Profile updated.')
            return redirect('blog:profile')
    else:
        pform = ProfileForm(instance=user.profile)
    return render(request, 'blog/profile.html', {'pform': pform})

# POSTS: List & Detail
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 10
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        tag = self.kwargs.get('tag', None)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)).distinct()
        if tag:
            qs = qs.filter(tags__name__iexact=tag)
        return qs

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.save(commit=True, author=self.request.user)
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        form.save(commit=True, author=self.request.user)
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# COMMENTS
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.author = request.user
            c.post = post
            c.save()
            messages.success(request, 'Comment added.')
    return redirect('blog:post-detail', pk=pk)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.request.object.post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.post.get_absolute_url()
