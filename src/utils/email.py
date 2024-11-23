from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse

from src.config.email_config import get_config_email
from src.language.ru_lang import Dictionary


settings = get_config_email()

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME = settings.MAIL_FROM_NAME,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
    # TEMPLATE_FOLDER = Path(__file__).parent.parent.parent.parent / 'frontend/template/email'
)


async def send_in_background_confirm(
    background_tasks: BackgroundTasks, email_to: str, body: dict) -> JSONResponse:
    message = MessageSchema(
        subject=Dictionary["message_subject"],
        recipients=[email_to],
        body=body,
        subtype='html',
    )    
    fm = FastMail(conf)
    background_tasks.add_task(
       fm.send_message, message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


async def send_email_confirm(email_to: str, body: dict) -> JSONResponse:
    message = MessageSchema(
        subject=Dictionary["message_subject"],
        recipients=[email_to],
        body=body,
        subtype='html',
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
