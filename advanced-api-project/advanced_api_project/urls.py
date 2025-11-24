from django.contrib import admin
from django.urls import path, include  # <- include is required

urlpatterns = [
    path('admin/', admin.site.urls),

    # <- This line must be present so Django knows about your API app
    path('api/', include('api.urls')),
]
