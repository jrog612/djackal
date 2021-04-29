from django.core.management import BaseCommand

from djackal.settings import djackal_settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        initializer = djackal_settings.INITIALIZER_CLASSE
        if not initializer:
            print('No initializers')

        print('Start initializing')
        initializer.run()
        print('Initialing done.')
