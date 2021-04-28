from djackal.exceptions import FieldException, DjackalAPIException, MessageException, NotFound
from djackal.tests import DjackalAPITestCase
from djackal.views.base import DjackalAPIView
from tests.models import TestModel


class TestException(DjackalAPIException):
    status_code = 501
    default_message = 'test_message'


class TestExceptionAPI(DjackalAPIView):
    def post(self, request):
        kind = request.data['kind']

        if kind == 'Message':
            raise MessageException(message=kind, test=True)
        elif kind == 'Field':
            raise FieldException(field=kind, message=kind, test=True)
        elif kind == 'NotFound':
            raise NotFound(model=TestModel, filters={'kind': kind}, test=True)

    def get(self, request):
        raise TestException()


class ExceptionTest(DjackalAPITestCase):
    def test_exception_handle(self):
        response = self.client.get('/exception')
        self.assertStatusCode(501, response)

    def test_exception_response(self):
        response = self.client.post('/exception', {'kind': 'Message'})
        result = response.json()
        self.assertEqual(result['test'], True)
        self.assertEqual(result['message'], 'Message')

        response = self.client.post('/exception', {'kind': 'Field'})
        result = response.json()
        self.assertEqual(result['test'], True)
        self.assertEqual(result['message'], 'Field')
        self.assertEqual(result['field'], 'Field')

        response = self.client.post('/exception', {'kind': 'NotFound'})
        result = response.json()
        self.assertEqual(result['test'], True)
        self.assertEqual(result['model'], 'TestModel')
        self.assertEqual(
            result['message'],
            NotFound.message_form.format(
                TestModel.__name__, 'kind=NotFound'
            )
        )
