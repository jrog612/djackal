from collections.abc import Iterable


def value_mapper(a_dict, b_dict):
    """
    a_dict = {
        'key1': 'a_value1',
        'key2': 'a_value2'
    }

    b_dict = {
        'key1': 'b_value1',
        'key2': 'b_value2'
    }

    >>> value_mapper(a_dict, b_dict)
    {
        'a_value1': 'b_value1',
        'a_value2': 'b_value2'
    }
    """

    return {a_value: b_dict.get(a_key) for a_key, a_value in a_dict.items()}


def islist(arg):
    """
    check arg is list or tuple or set not str or dict
    """
    return isinstance(arg, Iterable) and not isinstance(arg, (str, dict))


def isiter(arg):
    """
    check arg is list or tuple or set or dict not str
    """
    return isinstance(arg, Iterable) and not isinstance(arg, str)
