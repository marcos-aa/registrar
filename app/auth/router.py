from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .business import authenticate_user
from .schemas import TokenData
from app.db import get_db

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login", response_model=TokenData)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user_data = await authenticate_user(db, form_data.username, form_data.password)
    return user_data