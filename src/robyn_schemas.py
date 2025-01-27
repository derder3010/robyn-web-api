# Builtin robyn's schemas for showing on swaggerUI/openAPI and response.

from typing import Optional
from robyn.types import JSONResponse, Body


class RobynUserCreate(Body):
    username: str
    password: str


class RobynUserUpdate(Body):
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
