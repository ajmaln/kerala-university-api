from django.core.management.base import BaseCommand
from api.views import results_view
from api.models import Data

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        data = results_view(None, True)
        latest = None
        try:
            latest = Data.objects.latest()
            # Check for change

            if data == latest.json_data:
                self.stdout.write("No Change")
            else:
                # For now
                latest.json_data = data
                latest.save()
                # --- Notification Logic here ---
                self.stdout.write('Changed, sending notifications')
        except Data.DoesNotExist:
            latest = Data.objects.create(json_data=data)
        