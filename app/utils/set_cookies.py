from fastapi import Response
from app.config import settings

def set_jwt_cookies(
    response: Response,
    access_token: str,
    refresh_token: str
):
    response.set_cookie(
        key=settings.JWT_COOKIE_NAME,
        value=f"Bearer {access_token}",
        httponly=settings.JWT_COOKIE_HTTP_ONLY,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        domain=settings.JWT_COOKIE_DOMAIN,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    response.set_cookie(
        key=settings.JWT_REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=settings.JWT_COOKIE_HTTP_ONLY,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        domain=settings.JWT_COOKIE_DOMAIN,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 24 * 60 * 60
    )

def clear_jwt_cookies(response: Response):
    response.delete_cookie(settings.JWT_COOKIE_NAME)
    response.delete_cookie(settings.JWT_REFRESH_COOKIE_NAME)