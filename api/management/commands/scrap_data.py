from django.core.management.base import BaseCommand
from api.views import results_view, notifications_view, generic_view
from api.models import Data
from firebase_admin import messaging
from api.fcm import get_tokens


TYPES = ['results', 'notifications']


def compare_and_handle(type):
    # Scrap data from website
    latest = generic_view(None, True, type)
    
    try:
        # Get data stored in db
        data = Data.objects.filter(type=type).latest()

        # Compare both
        if latest == data.json_data:
            print("{}: No Change".format(type))
        else:
            data.json_data = latest
            data.save()
            print("{}: Changes detected, Sending notifications".format(type))
            message = messaging.Message(
                data={
                    'title': 'New {}'.format(type),
                    'body': 'New {} have been published!'.format(type)
                },
                topic=type
            )
            response = messaging.send(message)
            print(response)
    except Data.DoesNotExist:
        print('error')
        Data.objects.create(json_data=latest, type=type)


class Command(BaseCommand):

    def handle(self, *args, **options):
        list(map(compare_and_handle, TYPES))

        
