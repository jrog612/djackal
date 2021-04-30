from django.test import override_settings

from djackal.djadis.models import Djadis
from djackal.initializer import Initializer
from djackal.loaders import initializer_loader
from djackal.settings import djackal_settings
from djackal.tests import DjackalTestCase

initializer = Initializer()


@initializer.add('test')
def test_init_method():
    return 'test init result'


@initializer.add('test2')
def test_init_method():
    return 'test init result2'


class InitializerTest(DjackalTestCase):
    def test_initializer(self):
        assert len(initializer.init_methods) == 2
        assert initializer.init_methods['test']() == 'test init result'
        assert initializer.init_methods['test2']() == 'test init result2'
        assert Djadis.get('test_init') is not None
        assert Djadis.get('test2_init') is not None

    def test_initializer_load(self):
        with override_settings(DJACKAL={'INITIALIZER': 'tests.test_initializer.initializer'}):
            assert initializer_loader() is initializer

    def test_initializer_run(self):
        initializer.run()
        assert Djadis.get('test_init') is not None
        assert Djadis.get('test2_init') is not None
