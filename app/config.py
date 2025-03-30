from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str = "marcosandrade.it@gmail.com"
    EMAIL_PORT: int = 465
    EMAIL_SERVER: str = "smtp.gmail.com"

    class Config:
        env_file = ".env"

settings = Settings()