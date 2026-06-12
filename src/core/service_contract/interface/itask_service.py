from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union

from src.core.service_contract.data_model.task_data_model import TaskDataModel, TasksDataModel
from src.core.service_contract.enum.task_enum import TaskStatusEnum
from src.core.service_contract.enum.task_priority_enum import TaskPriorityEnum


class ITaskService(ABC):
    @abstractmethod
    def find(self, user_id: int, task_id: int) -> TaskDataModel:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, user_id: int, page_number: int, page_size: int, status: Union[TaskStatusEnum, None],
                priority: Union[TaskPriorityEnum, None]) -> TasksDataModel:
        raise NotImplementedError

    @abstractmethod
    def add(self, user_id: int, title: str, description: Union[str, None], due_date: Union[datetime, None],
            priority: TaskPriorityEnum, status: TaskStatusEnum) -> TaskDataModel:
        raise NotImplementedError

    @abstractmethod
    def soft_delete(self, user_id: int, task_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, user_id: int, task_id: int, title: str, description: Union[str, None],
               due_date: Union[datetime, None], priority: TaskPriorityEnum, status: TaskStatusEnum) -> TaskDataModel:
        raise NotImplementedError

    @abstractmethod
    def get_deleted_list(self, user_id: int) -> TasksDataModel:
        raise NotImplementedError

    @abstractmethod
    def active_deleted_task(self, user_id: int, task_id: int):
        raise NotImplementedError

    @abstractmethod
    def purge_deleted_tasks(self) -> int:
        raise NotImplementedError
