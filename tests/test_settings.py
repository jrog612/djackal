from django.test import TestCase, override_settings

from djackal.pagination import PageNumberPagination
from djackal.settings import DjackalSettings, djackal_settings


class TestSettings(TestCase):
    def test_settings_attr(self):
        assert djackal_settings.PAGE_SIZE == 10

    def test_import_error(self):
        settings = DjackalSettings({
            'DEFAULT_PAGINATION_CLASS': [
                'tests.invalid.PaginationClass'
            ]
        })
        with self.assertRaises(ImportError):
            print(settings.DEFAULT_PAGINATION_CLASS)

    def test_override_settings(self):
        with override_settings(DJACKAL={'PAGE_SIZE': 20}):
            assert djackal_settings.PAGE_SIZE == 20

        assert djackal_settings.PAGE_SIZE is 10

    def test_str_import(self):
        pagination = djackal_settings.DEFAULT_PAGINATION_CLASS
        assert pagination is PageNumberPagination
