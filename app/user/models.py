import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base 
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)

    user_codes = relationship("UserCode", back_populates="user")
    user_tokens = relationship("UserToken", back_populates="user")


class UserCode(Base):
    __tablename__ = "user_codes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    code = Column(String(6), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    user = relationship("User", back_populates="user_codes")

class UserToken(Base):
    __tablename__ = "user_token"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    user = relationship("User", back_populates="user_tokens")