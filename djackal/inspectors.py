from djackal.settings import djackal_settings


class remove:
    """
    When null is this class, that will removed in value dict.
    """
    pass


class InspectorException(Exception):
    def __init__(self, name, value, field):
        self.name = name
        self.value = value
        self.field = field


class Inspector:
    none_values = None
    """
    example of inspector map

    {
        'age': {
            'type': int,
            'null': 18,
            'required': true,
            'validator': ValidatorClass,
        },
    }
    """

    def __init__(self, target_dict, inspect_map):
        self.target = target_dict
        self.map = inspect_map

    def get_required_fields(self):
        return [key for key, value in self.map.items() if value.get('required', False)]

    def get_expected_fields(self):
        return self.map.keys()

    def get_type_fields(self):
        return {
            key: value.get('type') for key, value in self.map.items() if
            value.get('type') is not None
        }

    def get_validate_fields(self):
        return {
            key: value.get('validator') for key, value in self.map.items() if
            value.get('validator') is not None
        }

    def get_null_fields(self):
        return {
            key: value.get('null') for key, value in self.map.items() if
            value.get('null') is not None
        }

    def get_none_values(self):
        return self.none_values if self.none_values is not None else djackal_settings.DEFAULT_NONE_VALUES

    def remove_unexpected_fields(self, data):
        """
        Remove unexpected values.
        """
        fields = self.get_expected_fields()
        expected_dict = {key: value for key, value in data.items() if key in fields}
        return expected_dict

    def check_required(self, data):
        """
        Check required values are not contained or null
        """
        fields = self.get_required_fields()
        for req in fields:
            if data.get(req) in self.get_none_values():
                raise InspectorException(name=req, value=None, field='required')
        return True

    def convert_type(self, data):
        """
        Convert type to given function
        """
        fields = self.get_type_fields()
        ret_dict = dict()

        for key, value in data.items():
            if key in fields and value not in self.get_none_values():
                ret_dict[key] = fields[key](value)
                continue

            ret_dict[key] = value

        return ret_dict

    def check_validate(self, data):
        """
        Run given validater's is_valid function.
        """
        fields = self.get_validate_fields()
        for key, validator in fields.items():
            v = validator(value=data.get(key), field_name=key, total_data=data, inspector=self)
            if not v.is_valid():
                raise InspectorException(name=key, value=data.get(key), field='validator')
        return True

    def convert_null(self, data):
        """
        If value is none, convert given value of run function.
        """
        fields = self.get_null_fields()
        ret_dict = dict()

        for key, value in data.items():
            if key not in fields or value not in self.get_none_values():
                # Case - When value is not in none values: Add dict by passed value.
                ret_dict[key] = value
                continue

            if fields[key] is remove:
                # Case - When null value is remove class: Remove this key in dict.
                continue

            # Case - value is not exists or contained none values: Add default value.
            default = fields[key]
            ret_dict[key] = default() if callable(default) else default

        return ret_dict

    @property
    def inspected_data(self):
        ins_data = self.target
        ins_data = self.remove_unexpected_fields(ins_data)
        self.check_required(ins_data)
        ins_data = self.convert_type(ins_data)
        self.check_validate(ins_data)
        ins_data = self.convert_null(ins_data)
        return ins_data


class BaseValidator:
    """
    You can customize this validator. Please override is_valid function.
    """

    def __init__(self, value, field_name, **kwargs):
        self.value = value
        self.field_name = field_name
        self.kwargs = kwargs

    def is_valid(self):
        return True
