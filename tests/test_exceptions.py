from djackal.erra import Erra
from djackal.exceptions import DjackalAPIException, NotFound, Forbidden, BadRequest, InternalServer, ErraException
from djackal.tests import DjackalAPITestCase
from djackal.views.base import DjackalAPIView

TEST_FORBIDDEN_CODE = 'TEST_FORBIDDEN'
TEST_BAD_REQUEST_CODE = 'TEST_BAD_REQUEST'
TEST_INTERNAL_SERVER_CODE = 'TEST_INTERNAL_SERVER'

TEST_ERRA = Erra('TEST_ERRA', 'test_erra_message')


class TestException(DjackalAPIException):
    status_code = 501


class TestExceptionAPI(DjackalAPIView):
    def post(self, request):
        kind = request.data['kind']

        if kind == 'NotFound':
            raise NotFound(test=True)
        elif kind == 'Forbidden':
            raise Forbidden(code=TEST_FORBIDDEN_CODE, test=True)
        elif kind == 'BadRequest':
            raise BadRequest(code=TEST_BAD_REQUEST_CODE, test=True)
        elif kind == 'InternalServer':
            raise InternalServer(code=TEST_INTERNAL_SERVER_CODE, test=True)
        elif kind == 'Erra':
            raise ErraException(erra=TEST_ERRA, test=True)

    def get(self, request):
        raise TestException()


class ExceptionTest(DjackalAPITestCase):
    def test_exception_handle(self):
        response = self.client.get('/exception')
        self.assertStatusCode(501, response)

    def test_exception_response(self):
        response = self.client.post('/exception', {'kind': 'NotFound'})
        self.assertStatusCode(404, response)
        result = response.json()
        self.assertEqual(result['test'], True)
        self.assertEqual(result['code'], 'NOT_FOUND')

        response = self.client.post('/exception', {'kind': 'Forbidden'})
        self.assertStatusCode(403, response)
        result = response.json()
        self.assertEqual(result['test'], True)
        self.assertEqual(result['code'], TEST_FORBIDDEN_CODE)

        response = self.client.post('/exception', {'kind': 'BadRequest'})
        self.assertStatusCode(400, response)
        result = response.json()
        self.assertEqual(result['test'], True)
        self.assertEqual(result['code'], TEST_BAD_REQUEST_CODE)

        response = self.client.post('/exception', {'kind': 'InternalServer'})
        self.assertStatusCode(500, response)
        result = response.json()
        self.assertEqual(result['test'], True)
        self.assertEqual(result['code'], TEST_INTERNAL_SERVER_CODE)

        response = self.client.post('/exception', {'kind': 'Erra'})
        self.assertStatusCode(500, response)
        result = response.json()
        self.assertEqual(result['test'], True)
        self.assertEqual(result['code'], TEST_ERRA.code)
        self.assertEqual(result['message'], TEST_ERRA.message)
