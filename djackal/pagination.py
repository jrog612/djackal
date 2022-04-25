from rest_framework.pagination import PageNumberPagination as _PageNumberPagination, \
    LimitOffsetPagination as _LimitOffsetPagination, CursorPagination as _CursorPagination

from djackal.settings import djackal_settings


class BasePagination:
    def get_paginated_meta(self):
        raise NotImplementedError('get_paginated_meta() must be implemented.')


class PageNumberPagination(BasePagination, _PageNumberPagination):
    page_size = djackal_settings.PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = djackal_settings.MAX_PAGE_SIZE

    def get_paginated_meta(self):
        return {
            'count': self.page.paginator.count,
            'page': self.page.number,
        }


class LimitOffsetPagination(BasePagination, _LimitOffsetPagination):
    def get_paginated_meta(self):
        return {
            'count': self.count,
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
        }


class CursorPagination(BasePagination, _CursorPagination):
    def get_paginated_meta(self):
        return {
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
        }




