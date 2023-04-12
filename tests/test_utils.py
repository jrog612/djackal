from djackal.tests import DjackalTestCase
from djackal.utils import islist, value_mapper, isiter


class TestLoader(DjackalTestCase):
    def test_value_mapper(self):
        a_dict = {
            'key1': 'a_value1',
            'key2': 'a_value2',
        }

        b_dict = {
            'key1': 'b_value1',
            'key2': 'b_value2'
        }

        result = value_mapper(a_dict, b_dict)
        assert result[a_dict['key1']] == b_dict['key1']
        assert result[a_dict['key2']] == b_dict['key2']

    def test_islist(self):
        test_values = [
            ([1, 2, 3], True),
            ((1, 2, 3), True),
            ({1, 2, 3}, True),
            ({1: 1, 2: 2, 3: 3}, False),
            ('String Sentence', False),
            (None, False),
            (False, False),
            (True, False),
            (123, False),
        ]

        for val in test_values:
            self.assertIs(islist(val[0]), val[1])

    def test_isiter(self):
        test_values = [
            ([1, 2, 3], True),
            ((1, 2, 3), True),
            ({1, 2, 3}, True),
            ({1: 1, 2: 2, 3: 3}, True),
            ('String Sentence', False),
            (None, False),
            (False, False),
            (True, False),
            (123, False),
        ]

        for val in test_values:
            self.assertIs(isiter(val[0]), val[1])
