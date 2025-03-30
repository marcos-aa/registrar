from fastapi import Request, HTTPException
from sqlalchemy import update, select
from jose import jwt, JWTError
from app.security import create_token
from app.user.models import UserToken
from app.utils.set_cookies import set_jwt_cookies, clear_jwt_cookies
from app.config import settings
from datetime import datetime, timezone
from starlette.middleware.base import BaseHTTPMiddleware 

class JWTRefreshMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        is_session_expired = (
            response.status_code == 401 
            and "expired" in response.headers.get("www-authenticate", "")
        )

        if not is_session_expired:
            return response
        
        refresh_token = request.cookies.get(settings.JWT_REFRESH_COOKIE_NAME)
        
        if not refresh_token:
            clear_jwt_cookies(response)
            return response
            
        try:
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_REFRESH_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = payload["sub"]
            
            async with request.app.state.db.begin() as db:
                result = await db.execute(
                    select(UserToken)
                    .where(
                        UserToken.token == refresh_token,
                        UserToken.expires_at > datetime.now(timezone.utc)
                    )
                )
                if not result.scalar_one_or_none():
                    raise JWTError("Token revoked or expired")
                
                access_token, _ = create_token(user_id, 'access')
                refresh_token, expires_at = create_token(user_id, 'refresh')
                
                await db.execute(
                    update(UserToken)
                    .where(UserToken.token == refresh_token)
                    .values(
                        token=refresh_token,
                        expires_at=expires_at
                    )
                )
            
            set_jwt_cookies(
                response,
                access_token,
                refresh_token,
                request.app.state.settings
            )
            
            request.scope["auth_bypassed"] = True
            return await call_next(request)
            
        except JWTError:
            clear_jwt_cookies(response, request.app.state.settings)
            return response
