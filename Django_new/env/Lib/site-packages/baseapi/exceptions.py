class QueryException(Exception):
    def __init__(self, message, body=None, status_code=None, headers=None):
        super().__init__(message)
        self.body = body
        self.status_code = status_code
        self.headers = headers


class ClientException(Exception):
    pass
