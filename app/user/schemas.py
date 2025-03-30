from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str
    email: EmailStr
    is_active: bool

class UserCreate(BaseModel):
    email: EmailStr
    password: str