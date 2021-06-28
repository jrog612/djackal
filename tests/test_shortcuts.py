from django.test import override_settings

from djackal.exceptions import NotFound
from djackal.shortcuts import get_object_or_404, get_object_or_None, model_update, get_object_or, get_model, auto_f_key
from djackal.tests import DjackalTransactionTestCase
from tests.models import TestModel


class TestShortcuts(DjackalTransactionTestCase):
    def test_get_object_or(self):
        obj = TestModel.objects.create(field_int=1)

        self.assertIsNone(get_object_or_None(TestModel, field_int=2))
        self.assertEqual(get_object_or_None(TestModel, field_int=1), obj)

        with self.assertRaises(NotFound) as res:
            get_object_or_404(TestModel, field_int=2)

        self.assertIs(res.exception.model, TestModel)
        self.assertEqual(get_object_or_404(TestModel, field_int=1), obj)

        self.assertEqual('TestModel', get_object_or(TestModel, 'TestModel', field_int=2))
        self.assertEqual(obj, get_object_or(TestModel, 'TestModel', field_int=1))

    def test_model_update(self):
        obj = TestModel.objects.create(field_int=1, field_char='text')

        obj = model_update(obj, field_int=2, field_char='test2')

        self.assertEqual(obj.field_int, 2)
        self.assertEqual(obj.field_char, 'test2')

    def test_get_model(self):
        model = get_model('tests.TestModel')
        self.assertEqual(TestModel, model)

        with self.assertRaises(ValueError):
            get_model('TestModel')

        with override_settings(DJACKAL={
            'SINGLE_APP': True,
            'SINGLE_APP_NAME': 'tests'
        }):
            model = get_model('TestModel')
            self.assertEqual(TestModel, model)

    def test_auto_f_key(self):
        tm = TestModel.objects.create()

        self.assertEqual(auto_f_key(test_model=1), {'test_model_id': 1})
        self.assertEqual(auto_f_key(test_model=tm), {'test_model': tm})

        with self.assertRaises(ValueError):
            auto_f_key(test_model='TestModel'),
