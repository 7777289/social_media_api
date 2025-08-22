# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add this field to your existing User model
    following = models.ManyToManyField(
        "self",
        through="UserFollow",
        related_name="followers",
        symmetrical=False,
    )
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

class UserFollow(models.Model):
    user = models.ForeignKey(User, related_name="following_relations", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="follower_relations", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'follower')

    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"