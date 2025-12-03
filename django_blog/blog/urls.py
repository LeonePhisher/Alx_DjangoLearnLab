from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    # List all posts
    path('', PostListView.as_view(), name='post_list'),
     path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment_create'),

    # View single post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Create a new post
    path('post/new/', PostCreateView.as_view(), name='post_create'),

    # Update an existing post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),

    # Delete an existing post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]

