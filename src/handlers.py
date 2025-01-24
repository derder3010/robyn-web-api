# Logic CRUD

from sqlalchemy.orm import Session
from models import User
from sqlalchemy.exc import IntegrityError
from schemas import UserCreate


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


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
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


def update_user(db: Session, user_id: int, update_data):
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


def delete_user(db: Session, user_id: int):
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
