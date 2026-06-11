import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


class JWTUser:
    def __init__(self, payload: dict):
        self.id = payload.get("user_id")
        self.phone = payload.get("phone")
        self.role = payload.get("role")
        self.payload = payload

    @property
    def is_authenticated(self):
        return True


class CustomJWTAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode("utf-8")

        if not auth_header:
            return None

        try:
            keyword, token = auth_header.split()
        except ValueError:
            raise exceptions.AuthenticationFailed(
                "Invalid Authorization header. Use: Bearer <token>"
            )

        if keyword != self.keyword:
            raise exceptions.AuthenticationFailed(
                "Authorization header must start with Bearer"
            )

        payload = self.decode_token(token)
        user = JWTUser(payload)
        return user, token

    def decode_token(self, token: str) -> dict:
        if not settings.AUTH_SERVICE_SECRET_KEY:
            raise exceptions.AuthenticationFailed(
                "AUTH_SERVICE_SECRET_KEY is not configured"
            )
        try:
            payload = jwt.decode(
                token,
                settings.AUTH_SERVICE_SECRET_KEY,
                algorithms=settings.JWT_ALGORITHM,
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed("Invalid token signature")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        if payload.get("token_type") != "access":
            raise exceptions.AuthenticationFailed("Only access token is allowed")

        if not payload.get("user_id"):
            raise exceptions.AuthenticationFailed("Token does not contain user_id")

        return payload