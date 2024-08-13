
class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str = None, request_id: str = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.request_id = request_id
        super().__init__(message)


class InvalidRequest(AppError):
    def __init__(self, status_code=400,  code="InvalidRequest", message="Arguments are invalid.", request_id: str = None ):
        super().__init__(status_code, code, message)


class NotFound(AppError):
    def __init__(self, status_code=404, code="NotFound", message="Resource not found.", request_id: str = None):
        super().__init__(status_code, code, message)
    
class InternalServerError(AppError):
    def __init__(self, status_code=500, code="InternalServerError", message="Something went wrong.", request_id: str = None):
        super().__init__(status_code, code, message)
