class ServiceError(Exception):
    def __init__(self, message: str, error_code: str = "APPLICATION_ERROR"):
        """

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class TaskNotFoundError(ServiceError):
    def __init__(self, message: str = "Task not found"):
        super().__init__(message, error_code="TASK_NOT_FOUND")


class UserNotFoundError(ServiceError):
    def __init__(self, message: str = "User not found"):
        super().__init__(message, error_code="USER_NOT_FOUND")


class UserAlreadyExistsError(ServiceError):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message, error_code="USER_ALREADY_EXISTS")


class InvalidCredentialsError(ServiceError):
    def __init__(self, message: str = "Invalid username or password"):
        super().__init__(message, error_code="INVALID_CREDENTIALS")


class TokenExpiredError(ServiceError):

    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, error_code="TOKEN_EXPIRED")


class InvalidTokenError(ServiceError):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message, error_code="INVALID_TOKEN")


class UnauthorizedError(ServiceError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, error_code="UNAUTHORIZED")


class DatabaseError(ServiceError):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message=message, error_code="DATABASE_ERROR")
