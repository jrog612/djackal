import http
import random
import string

from rest_framework.test import APIRequestFactory

from djackal.exceptions import APIException, NotFound, Forbidden, BadRequest, InternalServer, \
    Unauthorized, NotAllowed
from djackal.tests import DjackalAPITestCase
from djackal.views.base import DjackalAPIView

TEST_BAD_REQUEST_CODE = 'TEST_BAD_REQUEST'
TEST_UNAUTHORIZED_CODE = 'TEST_UNAUTHORIZED'
TEST_FORBIDDEN_CODE = 'TEST_FORBIDDEN'
TEST_NOT_ALLOWED_CODE = 'TEST_NOT_ALLOWED'
TEST_INTERNAL_SERVER_CODE = 'TEST_INTERNAL_SERVER'
TEST_NOT_FOUND = 'NOT_FOUND'

factory = APIRequestFactory()


class TestException(APIException):
    default_status_code = 501


class ExceptionAPI(DjackalAPIView):
    def post(self, request):
        kind = request.data.get('kind')
        status_code = request.data.get('status_code')
        message = request.data.get('message')
        code = request.data.get('code')

        if kind == 'NotFound':
            raise NotFound(
                message=message,
                test=True,
                code=TEST_NOT_FOUND,
                status_code=status_code,
            )
        elif kind == 'BadRequest':
            raise BadRequest(
                message=message,
                code=code or TEST_BAD_REQUEST_CODE,
                test=True,
                status_code=status_code,
            )
        elif kind == 'Unauthorized':
            raise Unauthorized(
                message=message,
                code=code or TEST_UNAUTHORIZED_CODE,
                test=True,
                status_code=status_code,
            )
        elif kind == 'Forbidden':
            raise Forbidden(
                message=message,
                code=code or TEST_FORBIDDEN_CODE,
                test=True,
                status_code=status_code,
            )
        elif kind == 'NotAllowed':
            raise NotAllowed(
                message=message,
                code=code or TEST_NOT_ALLOWED_CODE,
                test=True
            )
        elif kind == 'InternalServer':
            raise InternalServer(
                message=message,
                code=code or TEST_INTERNAL_SERVER_CODE,
                test=True,
                status_code=status_code
            )
        else:
            raise APIException(
                message=message,
                code=code,
                test=True,
                status_code=status_code,
            )

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

        random_code = random.randint(100, 999)
        random_message = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=random.randint(12, 20)))

        request = factory.post('/', {
            'code': random_code,
            'message': random_message,
        })
        response = self.view(request)
        self.assertStatusCode(500, response)
        result = response.data
        self.assertEqual(result['test'], True)
        self.assertEqual(result['code'], str(random_code))
        self.assertEqual(result['message'], random_message)

    def test_exception_status_code(self):
        request = factory.post('/')
        response = self.view(request)
        self.assertStatusCode(500, response)

        code = random.choice(list(http.HTTPStatus))
        request = factory.post('/', {'status_code': code.value})
        response = self.view(request)
        self.assertStatusCode(code.value, response)
