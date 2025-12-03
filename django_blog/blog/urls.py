from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

app_name = 'blog'

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Posts
    path('', views.PostListView.as_view(), name='post-list'),
    path('search/', views.PostListView.as_view(), name='post-search'),  # q param handles search
    path('tags/<str:tag>/', views.PostListView.as_view(), name='posts-by-tag'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Comments
    path('posts/<int:pk>/comments/new/', views.add_comment, name='comment-create'),
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]

