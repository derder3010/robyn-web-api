from robyn.authentication import AuthenticationHandler
from robyn.robyn import Identity
import handlers
from db import SessionLocal
from robyn import Request


class BasicAuthHandler(AuthenticationHandler):
    def authenticate(self, request: Request):
        token = self.token_getter.get_token(request)
        if token is None:
            return
        try:
            payload = handlers.decode_access_token(token)
            username = payload["sub"]
        except Exception:
            return

        with SessionLocal() as db:
            user = handlers.get_user_by_username(db, username=username)

        return Identity(claims={"user": f"{ user }"})
