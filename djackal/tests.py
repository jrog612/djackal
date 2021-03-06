from django.db.models import QuerySet
from django.test import TransactionTestCase, TestCase
from rest_framework.test import APITestCase


class _TestMixin:
    def assertLen(self, length, seq):
        if isinstance(seq, QuerySet):
            assert length == seq.count()
        assert length == len(seq)

    def assertLenEqual(self, seq1, seq2):
        assert len(seq1) == len(seq2)

    def assertSuccess(self, response):
        assert 200 == response.status_code

    def assertStatusCode(self, code, response):
        assert code == response.status_code


class DjackalAPITestCase(APITestCase, _TestMixin):
    pass


class DjackalTransactionTestCase(TransactionTestCase, _TestMixin):
    pass


class DjackalTestCase(TestCase, _TestMixin):
    pass
