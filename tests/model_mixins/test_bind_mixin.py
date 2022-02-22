from django.db import models

from djackal.fields import JSONField
from djackal.model_mixins import BindMixin
from djackal.tests import DjackalTransactionTestCase


class TestBindModel(BindMixin, models.Model):
    bound_fields = ['b_field1', 'b_field2']
    extra = JSONField(default=dict)
    field_char = models.CharField(max_length=150, null=True)


class TestBindModel2(BindMixin, models.Model):
    bind_field_name = 'b_field'
    bound_fields = ['b_field1', 'b_field2']
    b_field = JSONField(default=dict)


class TestBindModel3(BindMixin, models.Model):
    bound_fields = {
        'b_field1': 'DEFAULT_VALUE',
        'b_field2': list,
    }
    extra = JSONField(default=dict)


class BindMixinTest(DjackalTransactionTestCase):
    def test_bind_values(self):
        tobj = TestBindModel()
        tobj.b_field1 = 'test_b_field1'
        tobj.field_char = 'char_field'
        tobj.save()
        tobj = TestBindModel.objects.get(id=tobj.id)
        self.assertEqual(tobj.b_field1, 'test_b_field1')
        self.assertEqual(tobj.extra, {'b_field1': 'test_b_field1'})
        self.assertIsNone(tobj.b_field2)
        self.assertEqual(tobj.field_char, 'char_field')
        with self.assertRaises(AttributeError):
            tobj.b_field3

    def test_different_bind_field_name(self):
        tobj = TestBindModel2()
        tobj.b_field1 = 'test_b_field1'
        tobj.save()
        tobj = TestBindModel2.objects.get(id=tobj.id)
        self.assertEqual(tobj.b_field1, 'test_b_field1')
        self.assertEqual(tobj.b_field, {'b_field1': 'test_b_field1'})
        self.assertIsNone(tobj.b_field2)
        with self.assertRaises(AttributeError):
            tobj.b_field3

    def test_create(self):
        tobj = TestBindModel.objects.create(
            b_field1='test_b_field1', field_char='char_field'
        )
        self.assertEqual(tobj.extra, {'b_field1': 'test_b_field1'})
        self.assertEqual(tobj.field_char, 'char_field')

    def test_dictionary_bound_fields(self):
        tobj = TestBindModel3.objects.create()

        self.assertEqual(tobj.b_field1, tobj.bound_fields['b_field1'])
        self.assertIs(type(tobj.b_field2), tobj.bound_fields['b_field2'])

        changed_value = 'CHANGED_VALUE'
        tobj.b_field1 = changed_value
        tobj.save()
        tobj.refresh_from_db()

        self.assertEqual(changed_value, tobj.b_field1)
