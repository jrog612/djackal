from djackal.exceptions import NotFound
from djackal.shortcuts import get_object_or_404, get_object_or_None, model_update, get_object_or
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
