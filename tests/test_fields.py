from django.db import models

from djackal.fields import JSONField
from djackal.tests import DjackalTransactionTestCase


class FieldTestModel(models.Model):
    json = JSONField(default=dict)


class FieldTest(DjackalTransactionTestCase):
    def test_json_field(self):
        test_dict = {'test_key': 'test_value'}

        tobj = FieldTestModel(json=test_dict)
        tobj.save()
        assert tobj.json == test_dict
        tobj = FieldTestModel.objects.first()
        assert tobj.json == test_dict

        tobj.json['test_key2'] = 'test_value2'
        tobj.save()

        assert tobj.json['test_key2'] == 'test_value2'
