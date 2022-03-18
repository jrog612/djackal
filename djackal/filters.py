from djackal.exceptions import NotFound
from djackal.loaders import param_funcs_loader
from djackal.shortcuts import gen_q
from djackal.utils import isiter


class DjackalQueryFilter:
    def __init__(self, queryset, params=None):
        self.queryset = queryset
        self.params = params or {}

    @staticmethod
    def _get_param_func(key):
        param_funcs = param_funcs_loader()
        matched = list(filter(lambda n: n == key, param_funcs.keys()))
        if matched:
            return param_funcs[matched[0]]
        return None

    def filter_map(self, filter_map):
        """
        params = {
            'name': 'Jrog',
            'age_lowest': '20',
            'skills': 'django,python',
            'status[]': [1, 2, 3],
        }
        f = DjackalQueryFilter(User.objects.all(), params)

        queryset = f.filter_map({
            'name': 'name__contains',
            'age_lowest': 'age__gte',
            'skills:to_list': 'skills__in',
            'status[]': 'status__in',
        }).queryset
        """

        queryset = self.queryset
        # initial
        filterable = {}
        filterable_q_objects = list()

        for map_key, filter_keyword in filter_map.items():
            # eg) map_key       : 'skills:to_list'
            #     filter_keyword: 'skills__in'
            split_key = map_key.split(':')
            if len(split_key) == 2:
                map_key = split_key[0]
                callback = self._get_param_func(split_key[1])
            else:
                callback = None

            # eg) map_key  : skills
            #     call_back: to_list function at DefaultQueryFunction
            if map_key.find('[]') > 0 and hasattr(self.params, 'getlist'):  # django drf query_params getlist support
                param_value = self.params.getlist(map_key)
                if param_value in [None, '', []]:
                    continue  # if empty, skip
            else:
                param_value = self.params.get(map_key)
            # eg) param_value  : 'django,python'

            if param_value in [None, '']:
                continue
            elif callback is not None:
                param_value = callback(param_value)
                # eg) param_value  : ['django', 'python']

            if isiter(filter_keyword):  # if filter_keyword is such like ('name__contains', 'job__contains').
                # make Q object like Q(Q(name__contains={param_value}) | Q(job__contains={param_value}))
                filterable_q_objects.append(gen_q(param_value, *filter_keyword))
            else:
                filterable[filter_keyword] = param_value

        self.queryset = queryset.filter(**filterable).filter(*filterable_q_objects)
        return self

    def search(self, search_dict, search_keyword_key='search_keyword', search_type_key='search_type'):
        """
        params = {
            'search_keyword': 'Yongjin',
            'search_type': 'name',
        }
        f = DjackalQueryFilter(User.objects.all(), params)

        queryset = f.search({
            'all': ('name__contains', 'job__contains', 'city__contains),
            'name': 'name__contains',
            'job': 'job__contains',
            'city': 'city__contains',
        }).queryset
        """

        queryset = self.queryset

        search_keyword = self.params.get(search_keyword_key)
        # if search_type is not exists, consider all type.
        search_type = self.params.get(search_type_key, 'all')
        # get search_type
        dict_value = search_dict.get(search_type, None)

        if dict_value is not None and search_keyword is not None:
            if isiter(dict_value):
                self.queryset = queryset.filter(gen_q(search_keyword, *dict_value))
            else:
                self.queryset = queryset.filter(**{dict_value: search_keyword})
        return self

    def extra(self, **extra_kwargs):
        """
        f = DjackalQueryFilter(User.objects.all(), {})
        queryset = f.extra(age__lte=30, is_active=True).queryset
        """

        queryset = self.queryset
        self.queryset = queryset.filter(**extra_kwargs)
        return self

    def ordering(self, ordering_map=None, ordering_key='ordering'):
        """
        if ordering_map exists:
            ordering_map = {
                'name': 'user__name'
            }
            params = {
                'ordering': 'name'
            }
        else:
            params = {
                'ordering': 'name,-age',
            }
        f = DjackalQueryFilter(User.objects.all(), params)

        queryset = f.ordering().queryset
        """

        ordering = self.params.get(ordering_key)
        if not ordering_map:
            order_value = ordering
        else:
            order_value = ordering_map.get(ordering, ordering)

        if order_value:
            queryset = self.queryset
            order_by = order_value.split(',')
            self.queryset = queryset.order_by(*order_by)
        return self

    def get(self, raise_404=False, **kwargs):
        """
        f = DjackalQueryFilter(User.objects.all(), {})
        user = f.get(id=5)
        """
        queryset = self.queryset
        obj = queryset.filter(**kwargs).first()
        if obj is None and raise_404:
            raise NotFound(model=queryset.model)

        return obj
