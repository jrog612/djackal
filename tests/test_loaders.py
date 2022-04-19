from django.test import override_settings

from djackal.tests import DjackalTestCase


class TestLoader(DjackalTestCase):
    def test_initializer_loader(self):
        with override_settings(DJACKAL={
            # 'INITIALIZER':
        }):
            pass
