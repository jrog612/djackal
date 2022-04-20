import http
import random

from rest_framework.test import APIRequestFactory

from djackal.erra import Erra
from djackal.exceptions import DjackalAPIException, NotFound, Forbidden, BadRequest, InternalServer, ErraException, \
    Unauthorized, NotAllowed
from djackal.tests import DjackalAPITestCase
from djackal.views.base import DjackalAPIView


class TestErra(Erra):
    TEST_ERRA = 'test_erra_message'


TEST_BAD_REQUEST_CODE = 'TEST_BAD_REQUEST'
TEST_UNAUTHORIZED_CODE = 'TEST_UNAUTHORIZED'
TEST_FORBIDDEN_CODE = 'TEST_FORBIDDEN'
TEST_NOT_ALLOWED_CODE = 'TEST_NOT_ALLOWED'
TEST_INTERNAL_SERVER_CODE = 'TEST_INTERNAL_SERVER'

factory = APIRequestFactory()


class TestException(DjackalAPIException):
    default_status_code = 501


class ExceptionAPI(DjackalAPIView):
    def post(self, request):
        kind = request.data['kind']
        status_code = request.data.get('status_code')

        if kind == 'NotFound':
            raise NotFound(test=True)
        elif kind == 'BadRequest':
            raise BadRequest(code=TEST_BAD_REQUEST_CODE, test=True)
        elif kind == 'Unauthorized':
            raise Unauthorized(code=TEST_UNAUTHORIZED_CODE, test=True)
        elif kind == 'Forbidden':
            raise Forbidden(code=TEST_FORBIDDEN_CODE, test=True)
        elif kind == 'NotAllowed':
            raise NotAllowed(code=TEST_NOT_ALLOWED_CODE, test=True)
        elif kind == 'InternalServer':
            raise InternalServer(code=TEST_INTERNAL_SERVER_CODE, test=True)
        elif kind == 'Erra':
            raise ErraException(erra=TestErra.TEST_ERRA, test=True, status_code=status_code)

    def get(self, request):
        raise TestException()


class ExceptionTest(DjackalAPITestCase):
    def setUp(self):
        self.view = ExceptionAPI.as_view()

    def test_exception_handle(self):
        request = factory.get('/')
        response = self.view(request)
        self.assertStatusCode(501, response)

    def _check_sub_erra_exception(self, kind, code, status_code):
        request = factory.post('/', {'kind': kind})
        response = self.view(request)
        self.assertStatusCode(status_code, response)
        result = response.data
        self.assertEqual(result['test'], True)
        self.assertEqual(result['code'], code)

    def test_exception_response(self):
        request = factory.post('/', {'kind': 'NotFound'})
        response = self.view(request)
        self.assertStatusCode(404, response)

        result = response.data
        self.assertEqual(result['test'], True)
        self.assertEqual(result['code'], 'NOT_FOUND')

        self._check_sub_erra_exception('BadRequest', TEST_BAD_REQUEST_CODE, 400)
        self._check_sub_erra_exception('Unauthorized', TEST_UNAUTHORIZED_CODE, 401)
        self._check_sub_erra_exception('Forbidden', TEST_FORBIDDEN_CODE, 403)
        self._check_sub_erra_exception('NotAllowed', TEST_NOT_ALLOWED_CODE, 405)

        request = factory.post('/', {'kind': 'Erra'})
        response = self.view(request)
        self.assertStatusCode(500, response)
        result = response.data
        self.assertEqual(result['test'], True)
        self.assertEqual(result['code'], TestErra.TEST_ERRA.code)
        self.assertEqual(result['message'], TestErra.TEST_ERRA.message)

    def test_exception_status_code(self):
        request = factory.post('/', {'kind': 'Erra'})
        response = self.view(request)
        self.assertStatusCode(500, response)
        code = random.choice(list(http.HTTPStatus))

        request = factory.post('/', {'kind': 'Erra', 'status_code': code.value})
        response = self.view(request)
        self.assertStatusCode(code.value, response)
