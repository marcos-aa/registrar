
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .schemas import TokenData
from app.user.models import User, UserToken

from app.security import verify_password, create_token

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