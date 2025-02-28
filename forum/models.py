from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field

# Identify the user roles
ROLE_CHOICES = [
    ('user', 'User'),
    ('moderator', 'Moderator'),
]
class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Unique related name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Unique related name
        blank=True,
        help_text="Specific permissions for the user.",
        verbose_name="user permissions",
    )
    def __str__(self):
        return self.username
    
    
class ForumTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class meta:
        verbose_name = 'Forum Tag'
        verbose_name_plural = 'Forum Tags'


class ForumPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    forum_tag = models.ForeignKey(ForumTag, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name='post_dislikes', blank=True)
    
    def __str__(self):
        return self.title
    
    class meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class ForumReply(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='reply_likes', blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name='reply_dislikes', blank=True)
    
    def __str__(self):
        return self.content
    
    class meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)


class Moderator(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    forum_tag = models.ForeignKey(ForumTag, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    Email = models.EmailField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=255,
        choices=[
            ("pending", "Pending"),
            ("active", "Active"),
            ("suspended", "Suspended"),
        ],
        default="pending",
    )

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Moderator'
        verbose_name_plural = 'Moderators'


# Add the Discussion model alias to maintain compatibility with the view functions
# This allows us to use the existing ForumPost model with the view functions that reference "Discussion"
Discussion = ForumPost

# Also make sure Comment is properly linked to discussions
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    discussion = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_comments', blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'







