from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, default='')  # Add default value
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='following',
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)  # Use default instead of auto_now_add
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()