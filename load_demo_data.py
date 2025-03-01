"""
Script to manually load demo data into the database.
Run this script directly when you need to populate the database with demo data.

Usage: python load_demo_data.py
"""
import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cybershield_project.settings')
django.setup()

# Now we can import Django models
from django.core.management import call_command
from django.contrib.auth import get_user_model
from forum.models import ForumTag, ForumPost, ForumReply, Comment, Moderator, UserProfile
from django.conf import settings
from django.db import connection, transaction
import traceback

def clear_existing_data():
    """Clear all existing data from the tables we're populating with demo data."""
    print("Clearing existing data...")
    
    try:
        # Use a transaction to ensure all deletions succeed or fail as a unit
        with transaction.atomic():
            # Delete in reverse order of dependencies to avoid constraint errors
            print("Deleting comments...")
            Comment.objects.all().delete()
            
            print("Deleting forum replies...")
            ForumReply.objects.all().delete()
            
            print("Deleting forum posts...")
            ForumPost.objects.all().delete()
            
            print("Deleting moderators...")
            Moderator.objects.all().delete()
            
            print("Deleting user profiles...")
            UserProfile.objects.all().delete()
            
            print("Deleting forum tags...")
            ForumTag.objects.all().delete()
            
            # Delete users last since they're referenced by other models
            User = get_user_model()
            
            print("Deleting regular users...")
            # Delete users from our fixture to avoid ID conflicts
            users_to_delete = [
                'admin', 'moderator1', 'moderator2', 'moderator3',
                'user1', 'user2', 'user3', 'user4', 'user5'
            ]
            User.objects.filter(username__in=users_to_delete).delete()
        
        print("All existing data cleared successfully.")
        return True
    except Exception as e:
        print(f"Error clearing data: {e}")
        traceback.print_exc()
        return False

def main():
    # Add a force option to bypass confirmation
    force = "-f" in sys.argv or "--force" in sys.argv
    
    # Check if we have users in the database
    User = get_user_model()
    if User.objects.exists() and not force:
        # If we already have users, ask for confirmation before overwriting
        confirmation = input("Database already contains data. Do you want to clear existing data and load demo data? (y/n): ")
        if confirmation.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Clear existing data
    if not clear_existing_data():
        print("Failed to clear existing data. Aborting.")
        return
    
    # Load the demo data from the fixture
    fixture_path = os.path.join(settings.BASE_DIR, 'demo.json')
    if not os.path.exists(fixture_path):
        print(f"Demo fixture not found at: {fixture_path}")
        return
    
    print(f"Loading demo data from {fixture_path}...")
    
    try:
        # Load the fixture
        call_command('loaddata', 'demo.json', verbosity=1)
        
        # Create a flag file to indicate data has been loaded
        flag_file = os.path.join(settings.BASE_DIR, '.demo_loaded')
        with open(flag_file, 'w') as f:
            f.write('Demo data loaded successfully')
        
        # Display counts of loaded data
        user_count = User.objects.count()
        tag_count = ForumTag.objects.count()
        post_count = ForumPost.objects.count()
        reply_count = ForumReply.objects.count()
        comment_count = Comment.objects.count()
        mod_count = Moderator.objects.count()
        
        print("\nDemo data loaded successfully:")
        print(f"- {user_count} users")
        print(f"- {mod_count} moderators")
        print(f"- {tag_count} forum tags")
        print(f"- {post_count} forum posts")
        print(f"- {reply_count} forum replies")
        print(f"- {comment_count} comments")
        print("\nYou can now access the superadmin account with:")
        print("Username: admin")
        print("Password: Abt123!!")
        
    except Exception as e:
        print(f"Error loading demo data: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()