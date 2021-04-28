from djackal.param_funcs import BaseParamFunc


class MyParamFunc(BaseParamFunc):
    @staticmethod
    def func_test_func(data):
        return True
