from celery import Celery

from src.config.celery_config import get_celery_settings

settings = get_celery_settings()


celery = Celery("mailing tasks")
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
