# SQLAlchemy models
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class RevokedToken(Base):
    __tablename__ = "removed_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    jti = Column(String(36), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)

    @classmethod
    def is_revoked(cls, db: Session, jti: str) -> bool:
        return (
            db.query(cls)
            .filter(cls.jti == jti, cls.expires_at > datetime.now(timezone.utc))
            .first()
            is not None
        )
