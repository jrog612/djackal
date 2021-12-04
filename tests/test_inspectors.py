from django.test import TestCase

from djackal.inspectors import Inspector, remove, InspectorException


class TestInspector(TestCase):
    def test_expected(self):
        pre_inspect = {
            'a': 'a',
            'b': 'a',
            'c': 'a',
            'd': 'a',
        }
        inspect_map = {
            'a': {},
            'b': {},
            'd': {}
        }
        ins = Inspector(pre_inspect, inspect_map)
        result = ins.inspected_data

        self.assertEqual({'a': 'a', 'b': 'a', 'd': 'a'}, result)
        self.assertNotIn('c', result)

    def test_required(self):
        pre_inspect = {
            'a': 'a',
            'c': 'a',
            'd': 'a',
        }
        inspect_map = {
            'a': {},
            'b': {'required': True},
            'd': {}
        }

        with self.assertRaises(InspectorException) as res:
            ins = Inspector(pre_inspect, inspect_map)
            ins.inspected_data
        self.assertEqual('b', res.exception.name)
        self.assertEqual('required', res.exception.field)

        pre_inspect.update({'b': 'a'})

        ins = Inspector(pre_inspect, inspect_map)
        result = ins.inspected_data
        self.assertEqual({'a': 'a', 'b': 'a', 'd': 'a'}, result)

    def test_convert(self):
        pre_inspect = {
            'a': 121,
            'b': '1234',
        }
        inspect_map = {
            'a': {'type': str},
            'b': {'type': int},
        }

        ins = Inspector(pre_inspect, inspect_map)
        result = ins.inspected_data
        self.assertEqual({'a': '121', 'b': 1234}, result)

    def test_default(self):
        pre_inspect = {
            'a': '',
            'b': None,
            'c': {},
            'd': [],
            'e': 'value',
        }
        inspect_map = {
            'a': {'default': remove},
            'b': {'default': None},
            'c': {'default': 'default'},
            'd': {'default': 100},
            'e': {},
            'f': {'default': 'NOT_EXISTS_DATA'},
        }

        ins = Inspector(pre_inspect, inspect_map)
        result = ins.inspected_data
        self.assertEqual({
            'b': None, 'c': 'default', 'd': 100, 'e': 'value', 'f': 'NOT_EXISTS_DATA'
        }, result)
