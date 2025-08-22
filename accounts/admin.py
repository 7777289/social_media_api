# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserFollow

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture')}),
    )
    list_display = UserAdmin.list_display + ('bio',)
    
    # We will display the counts as read-only fields instead
    readonly_fields = ['followers_count', 'following_count']
    
    def followers_count(self, obj):
        return obj.followers.count()
    
    def following_count(self, obj):
        return obj.following.count()


class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower', 'created_at')


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserFollow, UserFollowAdmin)