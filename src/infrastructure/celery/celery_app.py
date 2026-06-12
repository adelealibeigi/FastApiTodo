from celery import Celery

from src.infrastructure.config import settings

celery_app = Celery('worker', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BACKEND_URL)
celery_app.conf.update(
    broker_connection_retry_on_startup=True
)

celery_app.autodiscover_tasks([
    "src.infrastructure.celery.tasks"
])

