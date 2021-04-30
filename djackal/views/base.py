from rest_framework.response import Response
from rest_framework.views import APIView

from djackal import exceptions
from djackal.filters import DjackalQueryFilter
from djackal.inspectors import Inspector
from djackal.settings import djackal_settings
from djackal.utils import value_mapper


class BaseDjackalAPIView(APIView):
    default_permission_classes = ()
    default_authentication_classes = ()
    permission_classes = ()
    authentication_classes = ()

    result_root = 'result'
    result_meta = 'meta'

    inspect_map = {}
    inspector_class = Inspector

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_default_exception_handler(self):
        return djackal_settings.EXCEPTION_HANDLER

    def get_authentication_classes(self):
        return self.default_authentication_classes + self.authentication_classes

    def get_authenticators(self):
        return [auth() for auth in self.get_authentication_classes()]

    def get_permission_classes(self):
        return self.default_permission_classes + self.permission_classes

    def get_permissions(self):
        return [permission() for permission in self.get_permission_classes()]

    def pre_check_object_permissions(self, request, obj):
        pass

    def pre_check_permissions(self, request):
        pass

    def pre_handle_exception(self, exc):
        pass

    def pre_method_call(self, request, *args, **kwargs):
        pass

    def post_check_object_permissions(self, request, obj):
        pass

    def post_check_permissions(self, request):
        pass

    def post_method_call(self, request, response, *args, **kwargs):
        pass

    def get_inspector(self):
        inspect_map = self.get_cur_inspect_map()
        if not inspect_map:
            return None
        ins_class = self.inspector_class
        return ins_class(self.request.data, inspect_map)

    def get_inspected_data(self):
        inspector = self.get_inspector()
        if inspector is not None:
            return inspector.inspected_data
        return dict()

    def get_cur_inspect_map(self):
        return getattr(self, '{}_inspect_map'.format(self.request.method), self.inspect_map)

    def check_permissions(self, request):
        self.pre_check_permissions(request)
        super().check_permissions(request)
        self.post_check_permissions(request)

    def check_object_permissions(self, request, obj):
        self.pre_check_object_permissions(request, obj)
        super().check_object_permissions(request, obj)
        self.post_check_object_permissions(request, obj)

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            self.initial(request, *args, **kwargs)
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            self.pre_method_call(request, *args, **kwargs)
            response = handler(request, *args, **kwargs)
            self.post_method_call(request, response, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)

        return self.response

    def handle_exception(self, exc):
        """
        high jacking exception and handle with default_exception_handler
        """
        self.pre_handle_exception(exc)
        jackal_handler = self.get_default_exception_handler()
        context = self.get_exception_handler_context()
        response = jackal_handler(exc, context)
        if response is not None:
            response.exception = True
            return response
        else:
            return super().handle_exception(exc)

    def has_auth(self):
        return self.request.user is not None and self.request.user.is_authenticated

    def simple_response(self, result=None, status=200, meta=None, headers=None, **kwargs):
        response_data = {}

        if self.result_root:
            response_data[self.result_root] = result
            if self.result_meta:
                response_data[self.result_meta] = meta or dict()
        else:
            response_data = result or dict()

        return Response(response_data, status=status, headers=headers, **kwargs)


class DjackalAPIView(BaseDjackalAPIView):
    model = None
    queryset = None

    lookup_map = {}
    filter_map = {}
    search_dict = {}
    extra_kwargs = {}

    user_field = ''
    bind_user_field = None

    search_keyword_key = 'search_keyword'
    search_type_key = 'search_type'
    ordering_key = 'ordering'

    serializer_class = None
    query_filter_class = DjackalQueryFilter

    page_number_key = 'page_number'
    page_length_key = 'page_length'

    pagination_class = djackal_settings.DEFAULT_PAGINATION_CLASS
    paging = False

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if not self.paging:
                self._paginator = None
            else:
                if self.pagination_class is None:
                    self._paginator = None
                else:
                    self._paginator = self.pagination_class()
        return self._paginator

    def get_paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_meta(self):
        assert self.paginator is not None
        current_page = self.paginator.page

        return {
            'count': current_page.paginator.count,
            'previous': self.paginator.get_previous_link(),
            'next': self.paginator.get_next_link(),
        }

    def get_queryset(self):
        if self.queryset is not None:
            self.queryset = self.queryset.all()
            return self.queryset
        elif self.model is not None:
            return self.model.objects.all()
        raise exceptions.DjackalAPIException('JackalAPIView required model or queryset')

    def get_model(self):
        if self.model is not None:
            return self.model
        elif self.queryset is not None:
            return self.queryset.model
        raise exceptions.DjackalAPIException('JackalAPIView required model or queryset')

    def get_lookup_map(self, **additional):
        d = self.lookup_map or dict()
        return {**d, **additional}

    def get_filter_map(self, **additional):
        d = self.filter_map or dict()
        return {**d, **additional}

    def get_search_dict(self, **additional):
        d = self.search_dict or dict()
        return {**d, **additional}

    def get_extra_kwargs(self, **additional):
        d = self.extra_kwargs or dict()
        return {**d, **additional}

    def get_query_filter_class(self):
        if self.query_filter_class is None:
            return DjackalQueryFilter
        return self.query_filter_class

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self, **kwargs):
        return kwargs

    def get_serializer(self, instance, context=None, many=False, klass=None):
        if klass is None:
            klass = self.get_serializer_class()
        context = self.get_serializer_context(**(context or dict()))
        ser = klass(instance, many=many, context=context)
        return ser

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = self.get_user_queryset(queryset=queryset)

        f_class = self.get_query_filter_class()
        f = f_class(queryset=queryset, params=self.request.query_params)

        lookup_map = self.get_lookup_map()
        extra_kwargs = self.get_extra_kwargs(
            **value_mapper(lookup_map, self.kwargs)
        )

        obj = f.extra(**extra_kwargs).get(raise_404=True)
        self.check_object_permissions(request=self.request, obj=obj)
        return obj

    def get_filtered_queryset(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = self.get_user_queryset(queryset=queryset)

        f_class = self.get_query_filter_class()
        f = f_class(queryset=queryset, params=self.request.query_params)

        lookup_map = self.get_lookup_map()
        filter_map = self.get_filter_map()
        search_dict = self.get_search_dict()
        extra_kwargs = self.get_extra_kwargs()
        extra_kwargs.update(value_mapper(lookup_map, self.kwargs))

        queryset = f.search(
            search_dict,
            search_keyword_key=self.search_keyword_key,
            search_type_key=self.search_type_key
        ).filter_map(filter_map).extra(
            **extra_kwargs
        ).ordering(
            self.ordering_key
        ).queryset.distinct()
        return queryset

    def get_user_queryset(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        user_field = self.get_user_field()
        if user_field:
            queryset = queryset.filter(**{user_field: self.request.user})

        return queryset

    def get_user_field(self):
        return self.user_field

    def binding_user(self):
        return self.request.user
