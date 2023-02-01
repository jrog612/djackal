class ExtraMixin:
    extra_fields = ()
    extra_field_name = 'extra'

    def __init__(self, *args, **kwargs):
        self.extra_field_keys = tuple(self.extra_fields)
        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        if key in ('extra_fields', 'extra_field_name', 'extra_field_keys'):
            return super().__setattr__(key, value)
        if key in self.extra_field_keys:
            extra_hash = getattr(self, self.extra_field_name) or dict()
            extra_hash[key] = value
            return setattr(self, self.extra_field_name, extra_hash)
        return super().__setattr__(key, value)

    def __getattribute__(self, item):
        if item in ('extra_fields', 'extra_field_name', 'extra_field_keys'):
            return super().__getattribute__(item)
        elif item in self.extra_field_keys:
            extra_hash = getattr(self, self.extra_field_name) or dict()
            value = extra_hash.get(item)
            if value is None and type(self.extra_fields) is dict:
                default = self.extra_fields[item]
                value = default() if callable(default) else default
            return value

        return super().__getattribute__(item)
