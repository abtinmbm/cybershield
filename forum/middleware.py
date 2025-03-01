from django.core.management import call_command
import os
from django.conf import settings
from django.db import connection


class LoadDemoDataMiddleware:
    """
    Middleware to check and load demo data when the application is first accessed
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.data_loaded = False
        # Flag file path to track if we've loaded the data
        self.flag_file = os.path.join(settings.BASE_DIR, ".demo_loaded")

    def __call__(self, request):
        # Check if demo data has been loaded, but only once per server startup
        if not self.data_loaded and not os.path.exists(self.flag_file):
            try:
                self._load_demo_data()
                # Create a flag file to indicate we've loaded the data
                with open(self.flag_file, "w") as f:
                    f.write("Demo data loaded")
            except Exception as e:
                print(f"Error loading demo data: {e}")
            finally:
                self.data_loaded = True

        response = self.get_response(request)
        return response

    def _load_demo_data(self):
        try:
            # Try to load the demo data directly
            fixture_path = os.path.join(settings.BASE_DIR, "demo.json")
            if os.path.exists(fixture_path):
                print("Loading demo data...")
                call_command("loaddata", "demo.json", verbosity=1)
                print("Demo data loaded successfully!")
            else:
                print(f"Demo fixture not found at {fixture_path}")
        except Exception as e:
            print(f"Failed to load demo data: {e}")
