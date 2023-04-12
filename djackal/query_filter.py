from djackal.shortcuts import gen_q
from djackal.utils import islist


def to_bool(value):
    def checker(_value):
        if _value.lower() in ['true', 't', 'yes', 'y', 'on', '1']:
            return True
        elif _value.lower() in ['false', 'f', 'no', 'n', 'off', '0']:
            return False
        return None

    if islist(value):
        return list(checker(v) for v in value)
    return checker(value)


def qf_filter(queryset, field, value, key):
    if islist(field):
        return queryset.filter(gen_q(value, *field))
    else:
        return queryset.filter(**{field: value})


def qf_range(queryset, field, value, key):
    if islist(field):
        raise ValueError(f'action_range not allow multiple fields: {key}')

    if not islist(value):
        raise ValueError(f'action_range required list value not {value}: {key}')

    if len(value) != 2:
        raise ValueError(f'list length must be 2 not {len(value)}: {key}')

    return queryset.filter(
        **{
            f'{field}__gte': value[0],
            f'{field}__lte': value[1]
        }
    )


def filtering(queryset, params, schema):
    """
    query_schema = {
        'foo': 'var__contains',
        'foo': ('var__contains', 'var2__contains'),
        'foo': {
            'field': 'var' | ('var1', 'var2'),
            'allow_null': False,
            'format': format_func,
            'default': 'default_value',
            'action': 'filter' | 'range'
        }
    }
    """
    _queryset = queryset

    for schema_key, schema_value in schema.items():
        param_value = params.get(schema_key, None)
        is_value_none = param_value in [None, '', []]

        if type(schema_value) is not dict:
            if is_value_none:
                continue
            _queryset = qf_filter(_queryset, schema_value, params.get(schema_key, None), schema_key)
            continue

        if is_value_none:
            if 'default' in schema_value:
                param_value = schema_value['default']
            elif schema_value.get('allow_null'):
                param_value = None
            else:
                continue

        if 'field' not in schema_value:
            raise ValueError(f"'field' not found in schema: {schema_key}")

        field = schema_value['field']
        format_func = schema_value.get('format')
        if format_func:
            param_value = format_func(param_value)

        action = schema_value.get('action', qf_filter)
        if action == 'filter':
            action = qf_filter
        elif action == 'range':
            action = qf_range
        if not callable(action):
            raise ValueError(f'action method not exists: {schema_key}')

        _queryset = action(_queryset, field, param_value, schema_key)
    return _queryset
