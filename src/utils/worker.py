from email.message import EmailMessage
import smtplib

from celery import Celery

from src.config.celery_config import get_celery_settings
from src.logger import get_logger
from src.config.email_config import get_config_email
from src.language.ru_lang import Dictionary

settings = get_celery_settings()
email_settings = get_config_email()
logger = get_logger(__name__)


celery = Celery("celery")
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery.conf.broker_connection_retry_on_startup = True


@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, email_to: str, body: dict):
    message = EmailMessage()
    message["From"] = email_settings.MAIL_FROM
    message["To"] = email_to
    message["Subject"] = Dictionary["message_subject"]
    message.set_content(body)
    try:
        with smtplib.SMTP(email_settings.MAIL_SERVER, email_settings.MAIL_PORT) as server:
            server.starttls()
            server.login(email_settings.MAIL_FROM, email_settings.MAIL_PASSWORD)
            server.sendmail(email_settings.MAIL_FROM, email_to, message.as_string())
        return f"Email sent to {email_to}"
    except Exception as e:
        logger.info(f"ERROR {email_to}: {body}")
        raise self.retry(exc=e, contdown=5)
