from django.test import TestCase

from djackal.inspector import Inspector, skip, InspectActionException


class TestInspector(TestCase):
    def test_unknown(self):
        target = {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
        }
        inspect_map = {
            'one': {},
            'three': {},
            'four': {}
        }
        expected = {
            'one': 1,
            'three': 3,
            'four': 4,
        }
        ins = Inspector(inspect_map)
        result = ins.inspect(target)
        self.assertEqual(expected, result)

    def test_required(self):
        def _required_checker(key='three'):
            with self.assertRaises(InspectActionException) as res:
                ins.inspect(target)
            self.assertEqual(key, res.exception.key)
            self.assertEqual('required', res.exception.action)

        target = {
            'one': 0,
            'two': False,
            'three': 3,
            'four': 4,
        }
        inspect_map = {
            'one': {'required': True},
            'two': {'required': True},
            'three': {'required': True},
            'four': {},
        }
        ins = Inspector(inspect_map)

        for i in ['', None, [], {}]:
            target.update({'three': i})
            _required_checker()

        target.pop('three')
        _required_checker()

        target.update({'three': 3})
        result = ins.inspect(target)
        self.assertEqual(target, result)

    def test_convert(self):
        def _inner_convertor(value):
            return value.split(',')

        target = {
            'one': 123,
            'two': '1234',
            'three': 'one,two,three',
            'four': 0,
            'five': None,
        }
        inspect_map = {
            'one': {'convert': str},
            'two': {'convert': int},
            'three': {'convert': _inner_convertor},
            'four': {'convert': bool},
            'five': {'default': skip, 'convert': int}, # if skip not work, error raised.
        }
        expected = {
            'one': '123',
            'two': 1234,
            'three': ['one', 'two', 'three'],
            'four': False,
        }

        ins = Inspector(inspect_map)
        result = ins.inspect(target)
        self.assertEqual(expected, result)

    def test_type(self):
        def _type_checker(_key):
            with self.assertRaises(InspectActionException) as res:
                ins.inspect(target)
            self.assertEqual(_key, res.exception.key)
            self.assertEqual('type', res.exception.action)
            self.assertEqual(_key, res.exception.param)

        target = {
            'int': 123,
            'str': '123',
            'float': 0.123,
            'number': 123,
            'bool': False,
            'list': [1, 2, 3],
            'dict': {'key': 'value'}
        }
        inspect_map = {
            'int': {'type': 'int'},
            'str': {'type': 'str'},
            'float': {'type': 'float'},
            'number': {'type': 'number'},
            'bool': {'type': 'bool'},
            'list': {'type': 'list'},
            'dict': {'type': 'dict'},
        }
        ins = Inspector(inspect_map)
        result = ins.inspect(target)
        self.assertEqual(target, result)

        check_list = [
            ('int', 'string'),
            ('str', 123),
            ('float', 'string'),
            ('number', 'string'),
            ('bool', [1, 2, 3]),
            ('list', {'key': 'value'}),
            ('dict', 123),
        ]

        for key, value in check_list:
            target.update({key: value})
            _type_checker(key)
            target.pop(key)

    def test_default(self):
        target = {
            'one': '',
            'two': None,
            'three': {},
            'four': [],
            'five': 'value',
        }
        inspect_map = {
            'one': {'default': skip},
            'two': {'default': None},
            'three': {'default': 'default'},
            'four': {'default': 100},
            'five': {},
            'six': {'default': 'NOT_EXISTS_DATA'},
        }
        expected = {
            'two': None,
            'three': 'default',
            'four': 100,
            'five': 'value',
            'six': 'NOT_EXISTS_DATA'
        }

        ins = Inspector(inspect_map)
        result = ins.inspect(target)
        self.assertEqual(expected, result)

    def test_inspect(self):
        target = {
            'one': 123,
            'two': None,
            'three': 123,
            'four': 123,
        }
        inspect_map = {
            'one': {'required': True, 'type': 'int'},
            'two': {'type': 'str', 'default': 'default_str'},
            'three': {'required': True, 'convert': str},
            'four': {'type': 'int', 'convert': str},
        }
        expected = {
            'one': 123,
            'two': 'default_str',
            'three': '123',
            'four': '123',
        }

        ins = Inspector(inspect_map)
        result = ins.inspect(target)
        self.assertEqual(expected, result)
