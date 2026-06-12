from dataclasses import dataclass
from datetime import datetime
from typing import Union

from src.core.service_contract.enum.task_enum import TaskStatusEnum
from src.core.service_contract.enum.task_priority_enum import TaskPriorityEnum


@dataclass
class TaskDataModel:
    id: int
    title: str
    status: TaskStatusEnum
    priority: TaskPriorityEnum
    description: Union[str, None] = None
    due_date: Union[datetime, None] = None


@dataclass
class TasksDataModel:
    total_count: int
    tasks: list[TaskDataModel] = None
