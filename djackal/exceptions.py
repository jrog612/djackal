from rest_framework.exceptions import APIException
from rest_framework.response import Response


class DjackalAPIException(APIException):
    default_message = ''
    status_code = 500

    def __str__(self):
        return self.__class__.__name__

    def response_data(self):
        return {}


class ErraException(DjackalAPIException):
    def __init__(self, erra=None, code=None, message=None, context=None, **kwargs):
        self.erra = erra
        self.message = message
        self.code = code
        self.context = context
        self.kwargs = kwargs

    def response_data(self):
        if self.erra:
            response = self.erra.response_data(context=self.context)
        else:
            response = {'code': self.code, 'message': self.message}
        response.update(self.kwargs)
        return response


class NotFound(DjackalAPIException):
    status_code = 404
    default_message = 'Data not found'

    def __init__(self, message=None, context=None, model=None, **kwargs):
        self.context = context
        self.kwargs = kwargs
        self.model = model
        self.message = message or self.default_message

    def response_data(self):
        return {
            'code': 'NOT_FOUND',
            'message': self.message,
            **self.kwargs
        }


class BadRequest(ErraException):
    status_code = 400


class Unauthorized(ErraException):
    status_code = 401


class Forbidden(ErraException):
    status_code = 403


class NotAllowed(ErraException):
    status_code = 405


class InternalServer(ErraException):
    status_code = 500


def default_exception_handler(exc, context):
    if isinstance(exc, DjackalAPIException):
        return Response(exc.response_data(), status=exc.status_code)
    return None
