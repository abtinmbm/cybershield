from django.apps import AppConfig
import os


class ForumConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "forum"
    
    def ready(self):
        # Only run in the main process
        if os.environ.get('RUN_MAIN') != 'true':
            # Import needs to be here to avoid AppRegistryNotReady
            from django.contrib.auth import get_user_model
            from django.conf import settings
            import sys
            
            # Don't try to load data during migrations or when checking
            if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv and 'check' not in sys.argv:
                # We'll create a success flag file to avoid loading the data repeatedly
                flag_file = os.path.join(settings.BASE_DIR, '.demo_loaded')
                
                # Only load if flag file doesn't exist
                if not os.path.exists(flag_file):
                    # We need to ensure this runs in a request context
                    # Setting this up to be triggered on first request via middleware
                    pass
