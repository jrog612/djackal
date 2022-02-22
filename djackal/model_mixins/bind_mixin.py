class BindMixin:
    bound_fields = []
    bind_field_name = 'extra'

    def __init__(self, *args, **kwargs):
        self.bind_field_keys = list(self.bound_fields)
        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        if key in ['bound_fields', 'bind_field_name', 'bind_field_keys']:
            super().__setattr__(key, value)
            return
        if key in self.bind_field_keys:
            bind_hash = self.__bound_data
            bind_hash[key] = value
            setattr(self, self.bind_field_name, bind_hash)
            return
        else:
            super().__setattr__(key, value)
            return

    def __getattribute__(self, item):
        if item in ['bound_fields', 'bind_field_name', 'bind_field_keys']:
            return super().__getattribute__(item)
        elif item in self.bind_field_keys:
            bind_hash = self.__bound_data
            value = bind_hash.get(item)
            if value is None and type(self.bound_fields) is dict:
                default = self.bound_fields[item]
                value = default() if callable(default) else default
            return value
        else:
            return super().__getattribute__(item)

    @property
    def __bound_data(self):
        return getattr(self, self.bind_field_name, dict())
