from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads demo data from demo.json fixture'

    def handle(self, *args, **kwargs):
        fixture_path = os.path.join(settings.BASE_DIR, 'demo.json')
        if os.path.exists(fixture_path):
            self.stdout.write(self.style.SUCCESS('Loading demo data...'))
            call_command('loaddata', fixture_path)
            self.stdout.write(self.style.SUCCESS('Demo data loaded successfully!'))
        else:
            self.stdout.write(self.style.ERROR(f'Demo fixture not found at {fixture_path}'))