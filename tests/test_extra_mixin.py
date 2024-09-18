from django.db import models

from djackal.fields import JSONField
from djackal.model_mixins.extra_mixin import ExtraMixin
from djackal.tests import DjackalTransactionTestCase


class TestModel1(ExtraMixin, models.Model):
    extra_fields = ('b_field1', 'b_field2')
    extra = JSONField(default=dict)
    field_char = models.CharField(max_length=150, null=True)


class TestModel2(ExtraMixin, models.Model):
    extra_field_name = 'b_field'
    extra_fields = ('b_field1', 'b_field2')
    b_field = JSONField(default=dict)


class TestModel3(ExtraMixin, models.Model):
    extra_fields = {
        'b_field1': 'DEFAULT_VALUE',
        'b_field2': list,
    }
    extra = JSONField(default=dict)


class BindMixinTest(DjackalTransactionTestCase):
    def test_bind_values(self):
        tobj = TestModel1()
        tobj.b_field1 = 'test_b_field1'
        tobj.field_char = 'char_field'
        tobj.save()
        tobj = TestModel1.objects.get(id=tobj.id)
        self.assertEqual(tobj.b_field1, 'test_b_field1')
        self.assertEqual(tobj.extra, {'b_field1': 'test_b_field1'})
        self.assertIsNone(tobj.b_field2)
        self.assertEqual(tobj.field_char, 'char_field')
        with self.assertRaises(AttributeError):
            tobj.b_field3

        tobj.b_field2 = 'test_b_field2'
        tobj.save()
        tobj = TestModel1.objects.get(id=tobj.id)
        self.assertEqual(tobj.b_field2, 'test_b_field2')
        self.assertEqual(tobj.extra, {'b_field1': 'test_b_field1', 'b_field2': 'test_b_field2'})

    def test_different_bind_field_name(self):
        tobj = TestModel2()
        tobj.b_field1 = 'test_b_field1'
        tobj.save()
        tobj = TestModel2.objects.get(id=tobj.id)
        self.assertEqual(tobj.b_field1, 'test_b_field1')
        self.assertEqual(tobj.b_field, {'b_field1': 'test_b_field1'})
        self.assertIsNone(tobj.b_field2)
        with self.assertRaises(AttributeError):
            tobj.b_field3

    def test_dictionary_bound_fields(self):
        tobj = TestModel3.objects.create()

        self.assertEqual(tobj.b_field1, tobj.extra_fields['b_field1'])
        self.assertIs(type(tobj.b_field2), tobj.extra_fields['b_field2'])

        changed_value = 'CHANGED_VALUE'
        tobj.b_field1 = changed_value
        tobj.save()
        tobj.refresh_from_db()

        self.assertEqual(changed_value, tobj.b_field1)
