from email.message import EmailMessage
import smtplib
from datetime import datetime

from celery import Celery
from celery.schedules import crontab

from src.config.celery_config import get_celery_settings
from src.logger import get_logger
from src.config.email_config import get_config_email
from src.language.ru_lang import Dictionary
from src.utils.dependencies import UOWDep
from src.services.reservation_service import ReservationService
from src.services.temporary_reservation_service import TemporaryReservationService

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
        logger.error(f"ERROR {email_to}: {body}")
        raise self.retry(exc=e, contdown=5)


@celery.task
async def delete_oldest_reservations_task(uow: UOWDep):
    try:
        today = datetime.now().date()
        await ReservationService().remove_old_reservations(uow, today)
        await TemporaryReservationService().remove_old_reservations(uow, today)
        logger.info("Old records removed")
    except Exception as e:
        logger.error(f'ERROR ', exc_info=e)
        raise e

    
celery.conf.beat_schedule = {
    'delete-old-reservations': {
        'task': 'tasks.delete_oldest_reservations_task',
        'schedule': crontab(hour=2, minute=0)
    }
}