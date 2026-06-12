from datetime import datetime, timedelta, UTC
from typing import Union

from injector import inject

from src.core.exceptions.service_exceptions import TaskNotFoundError
from src.core.service_contract.data_model.task_data_model import TaskDataModel, TasksDataModel

from src.core.service_contract.enum.task_enum import TaskStatusEnum
from src.core.service_contract.enum.task_priority_enum import TaskPriorityEnum
from src.core.service_contract.interface.itask_service import ITaskService
from src.core.service_contract.interface.repository.itask_repository import ITaskRepository
from src.infrastructure.models.task_model import TaskModel
import logging

logger = logging.getLogger(__name__)


class TaskService(ITaskService):
    @inject
    def __init__(self, repository: ITaskRepository):
        self.__repository: ITaskRepository = repository

    def find(self, user_id: int, task_id: int) -> TaskDataModel:
        if model := self.__repository.get_model_by_id(task_id=task_id, user_id=user_id):
            return self.__make_task_data_model(model)
        raise TaskNotFoundError()

    @staticmethod
    def __make_task_data_model(model: TaskModel) -> TaskDataModel:
        priority = TaskPriorityEnum(model.priority)
        status = TaskStatusEnum(model.status)
        return TaskDataModel(
            id=model.id,
            title=model.title,
            description=model.description,
            due_date=model.due_date,
            priority=priority,
            status=status)

    def get_all(self, user_id: int, page_number: int, page_size: int, status: Union[TaskStatusEnum, None],
                priority: Union[TaskPriorityEnum, None]) -> TasksDataModel:
        priority = priority.value if priority else None
        status = status.value if status else None

        models, total_count = self.__repository.get_list_by_filter(user_id, page_number, page_size, status, priority)
        return self.__make_tasks_data_model(models, total_count)

    def __make_tasks_data_model(self, models: list[TaskModel], total_count: int) -> TasksDataModel:
        tasks_data_model_list = []
        for model in models:
            task_data_model = self.__make_task_data_model(model)
            tasks_data_model_list.append(task_data_model)
        return TasksDataModel(tasks=tasks_data_model_list, total_count=total_count)

    def add(self, user_id: int, title: str, description: Union[str, None], due_date: Union[datetime, None],
            priority: TaskPriorityEnum, status: TaskStatusEnum) -> TaskDataModel:
        priority = priority.value
        status = status.value
        model: TaskModel = TaskModel(
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status)
        model: TaskModel = self.__repository.add(model)
        task_data_model = self.__make_task_data_model(model)
        return task_data_model

    def update(self, user_id: int, task_id: int, title: str, description: Union[str, None],
               due_date: Union[datetime, None], priority: TaskPriorityEnum, status: TaskStatusEnum) -> TaskDataModel:
        priority = priority.value
        status = status.value
        if model := self.__repository.get_model_by_id(task_id=task_id, user_id=user_id):
            model.title = title
            model.description = description
            model.due_date = due_date
            model.priority = priority
            model.status = status
            model = self.__repository.update(model)
            task_data_model: TaskDataModel = self.__make_task_data_model(model)
            return task_data_model
        raise TaskNotFoundError()

    def soft_delete(self, user_id: int, task_id: int) -> None:

        if model := self.__repository.get_model_by_id(task_id=task_id, user_id=user_id):
            model.is_deleted = True
            model.deleted_at = datetime.now(UTC)
            self.__repository.set_soft_delete_status(model)
            return
        raise TaskNotFoundError()

    def get_deleted_list(self, user_id: int) -> TasksDataModel:
        models, total_count = self.__repository.get_list(user_id, is_deleted=True)
        return self.__make_tasks_data_model(models, total_count)

    def active_deleted_task(self, user_id: int, task_id: int):
        if model := self.__repository.get_model_by_id(task_id=task_id, user_id=user_id, is_deleted=True):
            model.is_deleted = False
            model.deleted_at = None
            self.__repository.set_soft_delete_status(model)
            return
        raise TaskNotFoundError()

    def purge_deleted_tasks(self) -> int:
        threshold = datetime.now(UTC) - timedelta(days=2)
        count = self.__repository.hard_delete(threshold)
        return count
