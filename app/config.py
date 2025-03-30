from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    SECRET_REFRESH_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080
    
    JWT_COOKIE_NAME: str = "access_token"
    JWT_REFRESH_COOKIE_NAME: str = "refresh_token"
    JWT_COOKIE_SECURE: bool = True  
    JWT_COOKIE_HTTP_ONLY: bool = True 
    JWT_COOKIE_SAMESITE: str = "strict"
    JWT_COOKIE_DOMAIN: str | None = "marcosandrade.dev"

    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str = "marcosandrade.it@gmail.com"
    EMAIL_PORT: int = 465
    EMAIL_SERVER: str = "smtp.gmail.com"

    class Config:
        env_file = ".env"

settings = Settings()