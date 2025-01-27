# Pydantic models for request validation

from pydantic import BaseModel, ConfigDict
import uuid
from typing import Optional
from robyn.types import JSONResponse, Body


class UserRegister(Body):
    username: str
    password: str


class RegisterResponse(JSONResponse):
    success: bool
    # id: uuid.UUID
    # username: str
    # is_active: bool
    # is_superuser: bool


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


class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[int] = None
    is_active: Optional[bool] = None
