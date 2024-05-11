from app.core.exceptions import BadRequest, NotAuthenticated, PermissionDenied


class AuthErrorCode:
    AUTHENTICATION_REQUIRED = "Authentication required."
    AUTHORIZATION_FAILED = "Authorization failed. User has no access."
    INVALID_TOKEN = "Invalid token."
    TOKEN_EXPIRED = "Token expired."
    INVALID_CREDENTIALS = "Invalid credentials."
    EMAIL_TAKEN = "Email is already taken."
    # REFRESH_TOKEN_NOT_VALID = "Refresh token is not valid."
    # REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie."


class AuthRequired(NotAuthenticated):
    DETAIL = AuthErrorCode.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = AuthErrorCode.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = AuthErrorCode.INVALID_TOKEN


class TokenExpired(NotAuthenticated):
    DETAIL = AuthErrorCode.TOKEN_EXPIRED


class InvalidCredentials(NotAuthenticated):
    DETAIL = AuthErrorCode.INVALID_CREDENTIALS


class EmailTaken(BadRequest):
    DETAIL = AuthErrorCode.EMAIL_TAKEN
