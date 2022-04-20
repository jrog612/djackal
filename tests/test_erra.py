import random

from djackal.erra import Erra
from djackal.tests import DjackalTestCase

CONTEXT_MESSAGE = 'Test Erra {num}'


class test(Erra):
    ERRA_ONE = 'Test Erra one'
    ERRA_TWO = 'Test Erra two'
    ERRA_CONTEXT = CONTEXT_MESSAGE


class ErraTest(DjackalTestCase):
    def test_get_message(self):
        random_int = random.randint(1, 100)
        message = test.ERRA_CONTEXT.get_message({'num': random_int})
        self.assertEqual(CONTEXT_MESSAGE.format(num=random_int), message)

    def test_response_data(self):
        response_data = test.ERRA_TWO.response_data()
        self.assertEqual(response_data, {'code': test.ERRA_TWO.code, 'message': test.ERRA_TWO.message})

    def test_str(self):
        self.assertEqual(str(test.ERRA_ONE), 'ERRA_ONE')
