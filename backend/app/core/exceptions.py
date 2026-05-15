from fastapi import HTTPException
from app.core.error_codes import ErrorCode, ERROR_MESSAGES


class AppException(HTTPException):
    def __init__(
        self,
        error_code: ErrorCode,
        detail: str | None = None,
        status_code: int = 400,
    ):
        self.error_code = error_code
        message = detail or ERROR_MESSAGES.get(error_code, "未知错误")
        super().__init__(status_code=status_code, detail={
            "error_code": error_code.value,
            "message": message,
        })


class NotFoundException(AppException):
    def __init__(self, error_code: ErrorCode, detail: str | None = None):
        super().__init__(error_code, detail, status_code=404)


class UnauthorizedException(AppException):
    def __init__(self, error_code: ErrorCode, detail: str | None = None):
        super().__init__(error_code, detail, status_code=401)


class ForbiddenException(AppException):
    def __init__(self, error_code: ErrorCode, detail: str | None = None):
        super().__init__(error_code, detail, status_code=403)


class DuplicateException(AppException):
    def __init__(self, error_code: ErrorCode, detail: str | None = None):
        super().__init__(error_code, detail, status_code=409)


class ValidationException(AppException):
    def __init__(self, error_code: ErrorCode, detail: str | None = None):
        super().__init__(error_code, detail, status_code=422)
