# social_media_api/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('post_comments.urls')),  # Update this line
    path('api-token-auth/', include('rest_framework.urls')),
]