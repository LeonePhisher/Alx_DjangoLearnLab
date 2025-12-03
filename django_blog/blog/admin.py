from django.contrib import admin
from .models import Post, Comment, Tag, Profile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Profile)
