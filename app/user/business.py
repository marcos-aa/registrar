from datetime import datetime, timezone
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, UserCode, UserToken
from . import schemas

from app.auth.business import manage_refresh_token

from app.utils.send_mail import create_user_code, send_verification_email
from app.security import get_password_hash, create_token

async def create_user(
        user_data: schemas.UserCreate,
        db: AsyncSession, 
        background_tasks: BackgroundTasks, 
    ) -> User:
    try:
        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password)
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        code = await create_user_code(db, user.id)
        await send_verification_email(user.email, code, background_tasks) 
        return user
    except Exception as e:
        raise HTTPException(status_code=403, detail="Email already registered")
    
async def verify_email(code: str, db: AsyncSession) -> schemas.UserToken:
    code_query = await db.execute(
        select(UserCode)
        .join(User)
        .options(selectinload(UserCode.user))
        .where(UserCode.code == code)
    )
    user_code = code_query.scalar_one_or_none()
    
    if not user_code:
        raise HTTPException(status_code=404, detail="Invalid code")
    
    now = datetime.now(timezone.utc)

    expires_at = datetime.fromisoformat(str(user_code.expires_at)).replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise HTTPException(status_code=403, detail="Expired code")
    
    user = user_code.user
    user.is_active = True

    access_token, _ = create_token(user.id, 'access')
    refresh_token = await manage_refresh_token(user.id, db)

    await db.delete(user_code)
    await db.commit()

    return {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "access_token": access_token,
        "refresh_token": refresh_token
    }