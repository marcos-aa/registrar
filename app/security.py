from datetime import datetime, timedelta, timezone
from typing import Optional, Literal
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_token(user_id: str, type: Literal['access', 'refresh']) -> tuple[str, datetime]:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id
    }
    if(type == 'access'):
        expires_at = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload["exp"] = expires_at
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token, expires_at
    else:
        expires_at = now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        payload["exp"] = expires_at
        token = jwt.encode(payload, settings.SECRET_REFRESH_KEY, algorithm=settings.ALGORITHM)
        return token, expires_at