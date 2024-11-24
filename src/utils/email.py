from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from fastapi.responses import JSONResponse

from src.config.email_config import get_config_email
from src.language.ru_lang import Dictionary
from src.utils.worker import celery

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


@celery.task(bind=True, max_retries=3, default_retry_delay=60)
async def send_email(self, email_to: str, body: dict) -> JSONResponse:
    try:
        message = MessageSchema(
            subject=Dictionary["message_subject"],
            recipients=[email_to],
            body=body,
            subtype='html',
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        raise self.retry(exc=e, contdown=5)
