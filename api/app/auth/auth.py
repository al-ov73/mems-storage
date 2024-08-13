from fastapi_users.authentication import CookieTransport, AuthenticationBackend, BearerTransport
from fastapi_users.authentication import JWTStrategy

from ..congif import JWT_SECRET_KEY

# cookie_transport = CookieTransport(cookie_name="memes", cookie_max_age=3600)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=JWT_SECRET_KEY, lifetime_seconds=3600)

# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(
#         secret=JWT_SECRET_KEY, 
#         lifetime_seconds=3600,
#         algorithm="RS256",
#         public_key=JWT_SECRET_KEY,
#     )

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
