from djackal.tests import DjackalTestCase
from djackal.utils import isiter, value_mapper


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

    def test_iterable(self):
        self.assertTrue(isiter([1, 2, 3]))
        self.assertTrue(isiter((1, 2, 3)))
        self.assertTrue(isiter({1, 2, 3}))
        self.assertTrue(isiter({1: 1, 2: 2, 3: 3}))

        self.assertFalse(isiter('String Sentence'))
        self.assertFalse(isiter(None))
        self.assertFalse(isiter(False))
        self.assertFalse(isiter(True))
        self.assertFalse(isiter(123))
