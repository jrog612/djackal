from rest_framework.pagination import PageNumberPagination as _PageNumberPagination, \
    LimitOffsetPagination as _LimitOffsetPagination, CursorPagination as _CursorPagination

from djackal.settings import djackal_settings


class PageNumberPagination(_PageNumberPagination):
    page_size = djackal_settings.PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = djackal_settings.MAX_PAGE_SIZE


class LimitOffsetPagination(_LimitOffsetPagination):
    pass


class CursorPagination(_CursorPagination):
    pass
