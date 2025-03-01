from forum.models import UserProfile, Moderator, CustomUser, ForumTag
from django.conf import settings
import os


# Function to fetch pulic resources along with user information
def get_public_resource_user():
    resources = []
    default_pic_url = settings.MEDIA_URL + 'DefaultPFP.jpg'
    
    # iterate over all user profiles
    for user_profile in UserProfile.objects.all():
        # Check if profile_pic exists and has an associated file
        if user_profile.profile_pic and hasattr(user_profile.profile_pic, 'url') and os.path.exists(os.path.join(settings.MEDIA_ROOT, user_profile.profile_pic.name)):
            profile_pic_url = user_profile.profile_pic.url
        else:
            profile_pic_url = default_pic_url
            
        resources.append(
            {
                "username": user_profile.username,
                "profile_pic": profile_pic_url,
                "bio": user_profile.bio,
                "is_moderator": False,  # Regular users are not moderators
                "role": "user"  # Default role
            }
        )
    return resources


# Function to fetch pulic resources along with moderator information
def get_public_resource_moderator():
    resources = []
    default_pic_url = settings.MEDIA_URL + 'DefaultPFP.jpg'
    
    # iterate over all moderators
    for moderator in Moderator.objects.filter(status="active").all():
        # Get the username as a string instead of a CustomUser object
        username = moderator.username.username if hasattr(moderator.username, 'username') else str(moderator.username)
        
        # Check if profile_pic exists and has an associated file
        if moderator.profile_pic and hasattr(moderator.profile_pic, 'url') and os.path.exists(os.path.join(settings.MEDIA_ROOT, moderator.profile_pic.name)):
            profile_pic_url = moderator.profile_pic.url
        else:
            profile_pic_url = default_pic_url
            
        # Get forum tag name for identifying the moderator's area of expertise
        forum_tag_name = ""
        if hasattr(moderator, 'forum_tag') and moderator.forum_tag:
            forum_tag_name = moderator.forum_tag.name

        resources.append(
            {
                "username": username,  # Use string username
                "profile_pic": profile_pic_url,
                "certifications": moderator.certifications if hasattr(moderator, 'certifications') else '',
                "bio": moderator.bio,
                "is_moderator": True,  # Mark as moderator
                "role": "moderator",  # Add role for styling
                "moderator_tag": forum_tag_name  # Add the tag they moderate
            }
        )
    return resources
