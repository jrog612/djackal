class Erra:
    def __init__(self, code, message=None):
        self.code = code
        self.message = message

    def __str__(self):
        return self.code

    def __eq__(self, other):
        other_type = type(other)

        if other_type is str:
            return self.code == other
        elif other_type is self.__class__:
            return self.code == other.code
        else:
            raise TypeError('Invalid type: {}'.format(other_type))

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_message(self, context=None):
        message = self.message
        if context and not message:
            message = message.format(**context)
        return message

    def response_data(self, context=None):
        message = self.get_message(context=context)
        return {'code': self.code, 'message': message}
