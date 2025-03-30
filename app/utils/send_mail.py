import random
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.user.models import UserCode
from app.config import settings
import os

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    TEMPLATE_FOLDER=os.path.join(os.path.dirname(__file__), 'templates')
)

env = Environment(loader=FileSystemLoader(conf.TEMPLATE_FOLDER))

async def send_verification_email(
    email: str,
    code: str,
    background_tasks: BackgroundTasks
):
    template = env.get_template("verification.html")
    html_content = template.render(code=code)
    
    message = MessageSchema(
        subject="Your Verification Code",
        recipients=[email],
        body=html_content,
        subtype="html"
    )
   
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)    

async def create_user_code(db: AsyncSession, user_id: str) -> str:
    code_query = await db.execute(
        select(UserCode)
        .where(UserCode.user_id == user_id)
    )
    existing_code = code_query.first()
    
    code = f"{random.randint(0, 999999):06d}"
    expires_at = datetime.now() + timedelta(minutes=15)
    
    if existing_code:
        await db.execute(
            update(UserCode)
            .where(UserCode.user_id == user_id)
            .values(
                code=code,
                expires_at=expires_at,
                created_at=datetime.now()
            )
        )
    else:
        db_code = UserCode(
            user_id=user_id,
            code=code,
            expires_at=expires_at
        )
        db.add(db_code)
    
    await db.commit()
    return code

