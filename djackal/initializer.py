from functools import wraps

from djackal.shortcuts import get_model


class Initializer:
    def __init__(self):
        self.initializers = []

    def wrapper(self, func, key, finish_message=None, skip_message=None):
        djadis_model = get_model('djadis.Djadis')
        if not djadis_model.get('{}_init'.format(key), False):
            func()
            djadis_model.set('{}_init'.format(key), True)
            print(finish_message or 'Finished {} initializing'.format(key))
        else:
            print(skip_message or 'Skip {} initializing'.format(key))

    def add(self, key, finish_message=None, skip_message=None):
        def decorator(func):
            self.initializers.append(func.__name__)

            @wraps(func)
            def inner():
                self.wrapper(func, key, finish_message, skip_message)
            return inner

        return decorator

    def run(self):
        for i in self.initializers:
            init_method = getattr(self, i)
            if not init_method:
                init_method()
