from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .schemas import UserCreate

from app.utils.send_mail import create_user_code, send_verification_email
from app.security import get_password_hash

async def create_user(
        user_data: UserCreate,
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