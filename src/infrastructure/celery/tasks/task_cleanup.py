from src.app_injector import app_injector
from src.core.service_contract.interface.itask_service import ITaskService
from src.infrastructure.celery.celery_app import celery_app


@celery_app.task(name="purge_deleted_tasks")
def purge_deleted_tasks():
    task_service: ITaskService = app_injector.get(ITaskService)
    task_service.purge_deleted_tasks()
