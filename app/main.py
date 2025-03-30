from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.user.router import user_router
from app.auth.router import auth_router

app = FastAPI(title="JWT Auth API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
