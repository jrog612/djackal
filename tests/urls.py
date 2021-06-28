from django.urls import path

from tests.test_exceptions import TestExceptionAPI

urlpatterns = [
    path('exception', TestExceptionAPI.as_view()),
]
