from fastapi import APIRouter, Depends, BackgroundTasks, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .business import authenticate_user, request_password_reset, reset_password
from .schemas import TokenData, RequestPasswordReset, PasswordReset
from app.db import get_db

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login", response_model=TokenData)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user_data = await authenticate_user(db, form_data.username, form_data.password)
    return user_data

@auth_router.post("/password-reset/request")
async def request_reset(
    data: RequestPasswordReset,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    message = await request_password_reset(db, data.email, background_tasks)
    return message


@auth_router.post("/password-reset/confirm", response_model=TokenData)
async def confirm_reset(
    data: PasswordReset,
    access_token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    user_data = await reset_password(db, access_token, data.password)
    return user_data

