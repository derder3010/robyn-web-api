from robyn.authentication import AuthenticationHandler
from robyn.robyn import Identity
import handlers
from db import SessionLocal
from robyn import Request
from models import RevokedToken
from jose import JWTError

# class BasicAuthHandler(AuthenticationHandler):
#     def authenticate(self, request: Request):
#         token = self.token_getter.get_token(request)
#         if token is None:
#             return
#         try:
#             payload = handlers.decode_access_token(token)
#             username = payload["sub"]
#         except Exception:
#             return
#
#         with SessionLocal() as db:
#             user = handlers.get_user_by_username(db, username=username)
#
#         return Identity(claims={"user": f"{ user }"})


class JWTAuthHandler(AuthenticationHandler):
    def authenticate(self, request: Request):
        token = self.token_getter.get_token(request)

        if not token:
            return None

        try:
            # Decode the token first
            payload = handlers.decode_access_token(token)
            username = payload["sub"]
            jti = payload["jti"]  # Get JWT ID from token
            exp = payload["exp"]

            if not username:
                print(f"No username or jti")
                return None

            # Check token revocation
            with SessionLocal() as db:
                # Check if token is revoked and still valid
                if RevokedToken.is_revoked(db, jti):
                    return None

                # Get user from database
                user = handlers.get_user_by_username(db, username=username)

                if not user:
                    return None

            # return Identity(claims={"user": f"{ user }"})

            return Identity(
                claims={
                    "user": f"{ user }",
                    "user_id": str(user.id),
                    "jti": str(jti),
                    "exp": str(exp),
                }
            )

        except JWTError:
            return None
