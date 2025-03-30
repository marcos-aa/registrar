from fastapi import APIRouter, Depends, BackgroundTasks, Body
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreate, User, UserToken
from .business import create_user, verify_email
from app.db import get_db

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("/", response_model=User)
async def register_user(
    user_data: UserCreate, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    user = await create_user(user_data, db, background_tasks)
    return user

@user_router.post("/verify", response_model=UserToken)
async def verify_user_email(
    code: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    user_token = await verify_email(code, db)
    return user_token