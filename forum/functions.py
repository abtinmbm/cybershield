from forum.models import UserProfile, Moderator, CustomUser, ForumTag


# Function to fetch pulic resources along with user information  
def get_public_resource_user():
    resources = []
    # iterate over all user profiles
    for user_profile in UserProfile.objects.all():
        resources.append({
            'username': user_profile.username,
            'profile_pic': user_profile.profile_pic.url,
            'bio': user_profile.bio,
        })
    return resources
   
# Function to fetch pulic resources along with moderator information

def get_public_resource_moderator():
    resources = []
    # iterate over all moderators
    for moderator in Moderator.objects.filter(status="active").all():
        resources.append({
            'username': moderator.username,
            'profile_pic': moderator.profile_pic.url,
            'certifications': moderator.certifications,
            'bio': moderator.bio,

        })
    return resources