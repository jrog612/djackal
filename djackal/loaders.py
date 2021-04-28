from djackal.param_funcs import BaseParamFunc
from djackal.settings import djackal_settings


def param_funcs_loader():
    ret_data = dict()
    for cls in djackal_settings.PARAM_FUNC_CLASSES:
        if issubclass(cls, BaseParamFunc):
            ret_data.update(cls.get_function_set())

    return ret_data
