from djackal.filters import BaseParamFunc


class MyParamFunc(BaseParamFunc):
    @staticmethod
    def func_test_func(data):
        return True
