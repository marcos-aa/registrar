
from fastapi import APIRouter, BackgroundTasks, Response, Request, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .business import authenticate_user, request_password_reset, reset_password, update_refresh_token
from .schemas import TokenData, RequestPasswordReset, PasswordReset, Token

from app.db import get_db
from app.utils.set_cookies import set_jwt_cookies, clear_jwt_cookies
from app.config import settings

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login", response_model=TokenData)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user_data, refresh_token = await authenticate_user(db, form_data.username, form_data.password)
    set_jwt_cookies(response, user_data["access_token"], refresh_token)
    return user_data

@auth_router.post("/logout")
async def logout(response: Response) -> dict:
    clear_jwt_cookies(response, settings)
    return {"message": "Logout successful"}


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
    response: Response,
    data: PasswordReset,
    access_token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    user_data, refresh_token = await reset_password(db, access_token, data.password)
    set_jwt_cookies(response, user_data["access_token"], refresh_token)
    return user_data

@auth_router.post("/refresh-token", response_model=Token)
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    refresh_token = request.cookies.get(settings.JWT_REFRESH_COOKIE_NAME)
    
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    token_data = await update_refresh_token(refresh_token, db)

    if not token_data:
        clear_jwt_cookies(response)
        raise HTTPException(status_code=401, detail="Invalid token")
    
    set_jwt_cookies(response, token_data.access_token, token_data.refresh_token)
    return {
        "token_type": "bearer",
        "access_token": token_data.access_token
    }

