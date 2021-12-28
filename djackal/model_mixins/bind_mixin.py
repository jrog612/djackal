class BindMixin:
    bound_fields = []
    bind_field_name = 'extra'

    def __init__(self, *args, **kwargs):
        self.bind_field_keys = list(self.bound_fields)
        given_bind_data = kwargs.pop(self.bind_field_name, dict())
        bind_data = {}
        for bound_field in self.bind_field_keys:
            value = kwargs.pop(bound_field, None)
            if value is None and type(self.bound_fields) is dict:
                default = self.bound_fields[bound_field]
                value = default() if callable(default) else default
            if value is not None:
                bind_data[bound_field] = value
        bind_data.update(given_bind_data)
        kwargs[self.bind_field_name] = bind_data
        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        if key in ['bound_fields', 'bind_field_name', 'bind_field_keys']:
            super().__setattr__(key, value)
            return
        if key in self.bind_field_keys:
            bind_hash = getattr(self, self.bind_field_name, dict())
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
            bind_hash = getattr(self, self.bind_field_name, dict())
            return bind_hash.get(item)
        else:
            return super().__getattribute__(item)
