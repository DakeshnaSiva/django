from ..utils import FileID


class Api:
    SUCCESS_RESPONSE_CODES = (200, 201)
    IGNORED_ATTRIBUTES = set([
        'expose_method',
        'make_variables',
        'check_file_id',
    ])

    @classmethod
    def expose_method(cls, method):
        method.expose = True
        return method

    def __init__(self, client):
        self.client = client

    def make_variables(self, **kwargs):
        return {
            key: value
            for key, value in kwargs.items()
            if value is not None
        }

    def check_file_id(self, file_id):
        if file_id is not None:
            if not isinstance(file_id, FileID):
                raise TypeError('File uploads must be FileID objects')
            file_id = str(file_id)
        return file_id
