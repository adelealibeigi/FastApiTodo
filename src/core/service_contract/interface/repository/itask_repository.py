from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union

from src.infrastructure.models.task_model import TaskModel


class ITaskRepository(ABC):
    @abstractmethod
    def get_model_by_id(self, user_id: int, task_id: int, is_deleted: bool = False) -> Union[TaskModel, None]:
        raise NotImplementedError

    @abstractmethod
    def get_list_by_filter(self, user_id: int, page_number: int, page_size: int, status: Union[int, None],
                           priority: Union[int, None]) -> tuple[list[TaskModel], int]:
        raise NotImplementedError

    @abstractmethod
    def update(self, model: TaskModel) -> TaskModel:
        raise NotImplementedError

    @abstractmethod
    def add(self, model: TaskModel) -> TaskModel:
        raise NotImplementedError

    @abstractmethod
    def set_soft_delete_status(self, model: TaskModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def hard_delete(self, before_date: datetime) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_list(self, user_id: int, is_deleted: bool = False) -> tuple[list[TaskModel], int]:
        raise NotImplementedError
