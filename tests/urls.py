from django.urls import path

from tests.views.test_extra import GetterResponseTestAPIView
from tests.views.test_filtering import FilteringTestAPI
from tests.test_exceptions import TestExceptionAPI

urlpatterns = [
    path('exception', TestExceptionAPI.as_view()),
]
