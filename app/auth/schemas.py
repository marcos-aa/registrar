from pydantic import BaseModel
from app.user.schemas import User
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(Token):
    user: User
class RefreshTokenRequest(BaseModel):
    refresh_token: str