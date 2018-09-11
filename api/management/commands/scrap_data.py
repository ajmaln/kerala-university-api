from django.core.management.base import BaseCommand
from api.views import results_view
from api.models import Data
from firebase_admin import messaging
from api.fcm import get_tokens


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
                message = messaging.Message(
                    data={
                        'title': 'New Results',
                        'body': 'New results have been announced!'
                    },
                    topic='results'
                )
                response = messaging.send(message)
                print(response)
                self.stdout.write('Changed, sending notifications')
        except Data.DoesNotExist:
            latest = Data.objects.create(json_data=data)


