from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreate, User
from .business import create_user
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
