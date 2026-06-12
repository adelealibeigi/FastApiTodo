from src.infrastructure.celery.celery_app import celery_app

from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "purge-deleted-tasks": {
        "task": "purge_deleted_tasks",
        "schedule": crontab(hour=0, minute=0),
    }
}
