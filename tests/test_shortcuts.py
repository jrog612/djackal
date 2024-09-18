import random

from django.test import override_settings

from djackal.shortcuts import get_object_or_None, model_update, get_object_or, get_model, auto_f_key, \
    gen_q
from djackal.tests import DjackalTransactionTestCase
from tests.models import TestModel


class TestShortcuts(DjackalTransactionTestCase):
    def test_get_object_or(self):
        obj = TestModel.objects.create(field_int=1)

        self.assertIsNone(get_object_or_None(TestModel, field_int=2))
        self.assertEqual(get_object_or_None(TestModel, field_int=1), obj)

        self.assertEqual('TestModel', get_object_or(TestModel, 'TestModel', field_int=2))
        self.assertEqual(obj, get_object_or(TestModel, 'TestModel', field_int=1))


def test_model_update(self):
    obj = TestModel.objects.create(field_int=1, field_char='text')

    obj = model_update(obj, field_int=2, field_char='test2')
    obj.refresh_from_db()

    self.assertEqual(obj.field_int, 2)
    self.assertEqual(obj.field_char, 'test2')

    obj = model_update(obj, field_int=4, field_char='test4', commit=False)
    obj.refresh_from_db()

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


def test_gen_q(self):
    random_int = random.randint(1, 100)
    random_char = f'random_char_{random_int}'
    tm1 = TestModel.objects.create(field_int=random_int)
    tm2 = TestModel.objects.create(field_char=random_char)
    TestModel.objects.create(field_char='WRONG')
    TestModel.objects.create(field_int=random_int + 100)

    qs = gen_q(random_int, 'field_int', 'field_char__contains')
    result = TestModel.objects.filter(qs)
    self.assertIn(tm1, result)
    self.assertIn(tm2, result)
    self.assertLen(2, result)


def test_auto_f_key(self):
    tm = TestModel.objects.create()

    self.assertEqual(auto_f_key(test_model=1), {'test_model_id': 1})
    self.assertEqual(auto_f_key(test_model=tm), {'test_model': tm})

    with self.assertRaises(ValueError):
        auto_f_key(test_model='TestModel'),
