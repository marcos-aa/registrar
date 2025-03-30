from pydantic import BaseModel
from app.user.schemas import User
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(Token):
    user: User

class RequestPasswordReset(BaseModel):
    email: str

class PasswordReset(BaseModel):
    password: str
class RefreshTokenRequest(BaseModel):
    refresh_token: str

class Tokens(Token):
    refresh_token: str