class BaseParamFunc:
    prefix = 'func'

    @classmethod
    def get_function_set(cls):
        ret_dict = {}

        for name, func in cls.__dict__.items():
            if name.find('{}_'.format(cls.prefix)) == 0:
                name = name.replace('{}_'.format(cls.prefix), '')
                ret_dict[name] = func.__func__
        return ret_dict


class DefaultParamFunc(BaseParamFunc):
    @staticmethod
    def func_to_list(data):
        return data.split(',')

    @staticmethod
    def func_to_bool(data):
        return data.lower() == 'true'
