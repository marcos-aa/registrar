
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from sqlalchemy import select
from .schemas import TokenData

from app.user.models import User, UserToken
from app.utils.send_mail import send_password_reset_email
from app.security import verify_password, get_password_hash, create_token
from app.config import settings

from datetime import datetime, timedelta, timezone

async def authenticate_user(db: AsyncSession, email: str, password: str) -> TokenData:
    user_query = await db.execute(select(User).where(User.email == email))
    user = user_query.scalar_one_or_none()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account not verified")
    
    access_token, _ = create_token(user.id, "access")
    await manage_refresh_token(user.id, db)

    await db.commit()
    
    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "is_active": user.is_active,
            "email": user.email
        }
    }

async def request_password_reset(
    db: AsyncSession,
    email: str,
    background_tasks: BackgroundTasks
) -> dict:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    message = {"message": "A password reset link has been sent to your inbox"}
    if not user or user.is_active == False:
        return message

    now = datetime.now(timezone.utc)
    reset_token_exp = now + timedelta(minutes=60)
    access_token, _ = create_token(user.id, 'access', reset_token_exp)

    await send_password_reset_email(email, access_token, background_tasks)

    return message

async def reset_password(
    db: AsyncSession,
    token: str,
    new_password: str
) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid token")
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.hashed_password = get_password_hash(new_password)
        
        access_token, _ = create_token(user.id, 'access')
        refresh_token = manage_refresh_token(user.id, db)
        
        await db.commit()
        
        return {
            "token_type": 'bearer',
            "access_token": access_token,
            "user": user
        }
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Expired reset link")
    except jwt.JWTError as e:
        raise HTTPException(status_code=400, detail=f"Invalid reset link: {str(e)}")

async def manage_refresh_token(user_id: str, db = AsyncSession) -> str:
    ref_token_query = await db.execute(
        select(UserToken).where(UserToken.user_id == user_id)
    )

    existing_token = ref_token_query.scalar_one_or_none()

    refresh_token, expires_at = create_token(user_id, "refresh")

    if existing_token:
        existing_token.token = refresh_token
        existing_token.expires_at = expires_at
    else:
        db_refresh = UserToken(
            user_id=user_id,
            token=refresh_token,
            expires_at=expires_at
        )
        db.add(db_refresh)
    
    return refresh_token