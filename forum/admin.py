from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from django.contrib.auth.models import User, Group
from .forms import UserCreationForm, ModeratorCreationForm, CreateForumPostForm
from .models import ForumPost, ForumTag, ForumReply, CustomUser, Moderator
from django.contrib.admin import site
from django.db.models.signals import post_migrate
from django.dispatch import receiver

site.disable_action('delete_selected')

# Create initial forum tags if they don't exist
def create_initial_forum_tags():
    tags = ["Phishing", "Ransomware", "DDoS", "Malware", "Security News", 
            "Data Breaches", "Social Engineering", "Network Security", 
            "Zero-day Exploits", "Cryptography", "Identity Theft"]
    
    for tag in tags:
        ForumTag.objects.get_or_create(name=tag)

# Use a signal to run this after migrations are complete
@receiver(post_migrate)
def create_tags_after_migrations(sender, **kwargs):
    if sender.name == 'forum':  # Only run for the forum app
        create_initial_forum_tags()
        
# DO NOT call create_initial_forum_tags() directly here

class ForumTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'forum_tag', 'created_at')
    list_filter = ('forum_tag', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is superuser, show all posts
        if request.user.is_superuser:
            return qs
        # For moderators, show only posts they can moderate
        return qs

class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is superuser, show all replies
        if request.user.is_superuser:
            return qs
        # For moderators, show only replies they can moderate
        return qs

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is superuser, show all users
        if request.user.is_superuser:
            return qs
        # For moderators, show only regular users
        return qs.filter(role='user')
    
    def has_change_permission(self, request, obj=None):
        # Only allow superusers or the user themselves to edit user profiles
        if not obj:
            return True
        return request.user.is_superuser or request.user == obj.username

class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('username', 'Email', 'status')
    list_filter = ('status',)
    search_fields = ('username', 'Email')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only superusers can see and manage moderators
        if not request.user.is_superuser:
            return qs.none()
        return qs
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        return request.user.is_superuser

# Register models
admin.site.register(ForumTag, ForumTagAdmin)
admin.site.register(ForumPost, ForumPostAdmin)
admin.site.register(ForumReply, ForumReplyAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Moderator, ModeratorAdmin)