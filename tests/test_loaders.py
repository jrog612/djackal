from django.test import override_settings

from djackal.loaders import param_funcs_loader
from djackal.param_funcs import DefaultParamFunc
from djackal.settings import default_param_func
from djackal.tests import DjackalTestCase
from tests.param_funcs import MyParamFunc


class TestLoader(DjackalTestCase):
    def test_param_func_loader(self):
        with override_settings(DJACKAL={
            'PARAM_FUNC_CLASSES': [
                'tests.param_funcs.MyParamFunc',
                default_param_func,
            ]
        }):
            funcs = param_funcs_loader()

            self.assertIs(funcs['to_bool'], DefaultParamFunc.func_to_bool)
            self.assertIs(funcs['to_list'], DefaultParamFunc.func_to_list)
            self.assertIs(funcs['test_func'], MyParamFunc.func_test_func)
