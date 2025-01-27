# Logic CRUD
from typing import Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from models import User, RevokedToken
from sqlalchemy.exc import IntegrityError
from schemas import UserCreate
from jose import JWTError, jwt
import uuid

# SOLVE PASSLIB WARNING ########################################################
from dataclasses import dataclass
import bcrypt
from passlib.context import CryptContext


@dataclass
class SolveBugBcryptWarning:
    __version__: str = getattr(bcrypt, "__version__")


setattr(bcrypt, "__about__", SolveBugBcryptWarning())
################################################################################

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12, deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


ALGORITHM = "HS256"
SECRET_KEY = "your_secret_key"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encoded = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encoded.update(
        {
            "exp": expire,
            "jti": str(uuid.uuid4()),
        }
    )
    encode_jwt = jwt.encode(to_encoded, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    created_token = create_access_token(data={"sub": username})
    return created_token


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_data: UserCreate):
    try:
        if db.query(User).filter(User.username == user_data.username).first():
            raise ValueError("Username already exists")

        db_user = User(
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Username already exists")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to create user: {str(e)}")


def logout_user(db: Session, decoded_token):
    try:
        jti = decoded_token["jti"]
        exp = datetime.fromtimestamp(int(decoded_token["exp"]), tz=timezone.utc)

        if RevokedToken.is_revoked(db, jti):
            raise ValueError("Token already revoked")

        db.add(RevokedToken(jti=jti, expires_at=exp))
        db.commit()
        return {"message": "Successfully logged out"}
    except JWTError:
        raise JWTError


def update_user(db: Session, user_id: str, update_data):
    try:
        db_user = get_user(db, user_id)
        if db_user is None:
            raise ValueError("User not found")
        update_dict = update_data.model_dump(exclude_unset=True)

        # Handle password hashing
        if "password" in update_dict:
            update_dict["hashed_password"] = get_password_hash(
                update_dict.pop("password")
            )

        valid_fields = User.__table__.columns.keys()
        for key, value in update_dict.items():
            if key not in valid_fields:
                raise ValueError(f"Invalid field: {key}")
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower():
            raise ValueError("Username already exists")
        raise
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to update user: {str(e)}")


def delete_user(db: Session, user_id: str):
    try:
        db_user = get_user(db, user_id)
        if db_user is None:
            raise ValueError("User not found")
        db.delete(db_user)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to delete user: {str(e)}")
