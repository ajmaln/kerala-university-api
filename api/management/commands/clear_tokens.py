from api.fcm import get_tokens, get_details, db
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        for token in get_tokens():
            if get_details(token).get('error', False):
                db.document('tokens/{}'.format(token)).delete()
        print('Tokens cleared')

