from rest_framework.exceptions import APIException as _APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


class APIException(_APIException):
    default_message = None
    default_code = None
    default_status_code = 500

    def __init__(self, message=None, code=None, status_code=None, **kwargs):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.kwargs = kwargs

    def __str__(self):
        return self.message

    def response_data(self):
        result = {
            'message': self.get_message(),
            **self.kwargs,
        }
        code = self.get_code()
        if code is not None:
            result['code'] = code
        return result

    def get_message(self):
        return self.message or self.default_message

    def get_code(self):
        return self.code or self.default_code

    def get_status_code(self):
        return self.status_code or self.default_status_code


class NotFound(APIException):
    default_status_code = 404
    default_message = 'not found'


class BadRequest(APIException):
    default_status_code = 400
    default_message = 'bad request'


class Unauthorized(APIException):
    default_status_code = 401
    default_message = 'unauthorized'


class Forbidden(APIException):
    default_status_code = 403
    default_message = 'forbidden'


class NotAllowed(APIException):
    default_status_code = 405
    default_message = 'not allowed'


class InternalServer(APIException):
    default_status_code = 500
    default_message = 'internal server error'


class PermissionException(APIException):
    default_status_code = 403
    default_message = 'permission denied'

    def __init__(self, permission, message=None, code=None, status_code=None, **kwargs):
        super().__init__(
            message=message,
            code=code,
            status_code=status_code,
            **kwargs
        )
        self.permission = permission


def exception_handler(exc, context):
    if isinstance(exc, APIException):
        return Response(exc.response_data(), status=exc.get_status_code())
    return drf_exception_handler(exc, context)
