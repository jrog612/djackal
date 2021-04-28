from django.core.management import BaseCommand, CommandError

from djackal.initializer import Initializer
from djackal.settings import djackal_settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        initializers = djackal_settings.INITIALIZER_CLASSES
        if not initializers:
            print('No initializers')

        print('Start initializing')
        for i in initializers:
            if not issubclass(i, Initializer):
                raise CommandError(
                    '{} is not subclass of Initializer.'.format(i.__name__))
            initializer = i()
            initializer.run()
        print('Initialing done.')
