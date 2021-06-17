from django.urls import path

from tests.views.test_api_vew import FilteringTestAPI
from tests.test_exceptions import TestExceptionAPI

urlpatterns = [
    path('exception', TestExceptionAPI.as_view()),
    path('filtering', FilteringTestAPI.as_view()),
]
