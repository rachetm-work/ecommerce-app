class BaseCustomException(Exception):
    """Base class for custom exception. """

    def __init__(self, error_message, status, code):
        super().__init__(error_message)
        self.error_message = error_message
        self.status = status
        self.code = code

    def __str__(self):
        return f'{self.__class__.__name__}: {self.error_message}'


class BadRequest(BaseCustomException):
    """Exception that represents a request that was made with an invalid format."""

    def __init__(self, error_message='Bad Request', status=400, code='bad_request'):
        super().__init__(error_message, status, code)


class ServerError(BaseCustomException):
    """ Exception that represents any generic internal server error."""

    def __init__(self, error_message='Server Error', status=500, code='server_error'):
        super().__init__(error_message, status, code)
