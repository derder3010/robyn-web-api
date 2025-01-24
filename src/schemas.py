# Pydantic models response

from pydantic import BaseModel, ConfigDict
import uuid
from typing import Optional


# Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)
