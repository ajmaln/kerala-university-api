from django.core.management.base import BaseCommand
from api.views import results_view
from api.models import Data
from firebase_admin import messaging
from api.fcm import get_tokens


class Command(BaseCommand):

    def handle(self, *args, **options):
        messaging.subscribe_to_topic(list(get_tokens()), 'results')
        print('subscriptions updated')


