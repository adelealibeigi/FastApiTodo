from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

from src.core.service_contract.data_model.task_data_model import TaskDataModel


class TaskStatusEnumSchema(str, Enum):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class TaskPriorityEnumSchema(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskFilterSchema(BaseModel):
    model_config = ConfigDict(use_enum_values=False)
    status: Optional[TaskStatusEnumSchema] = None
    priority: Optional[TaskPriorityEnumSchema] = None


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=150, min_length=3, description="Title of the task")
    description: Optional[str] = Field(None, max_length=500, min_length=5, description="Description of the task")
    due_date: Optional[datetime] = Field(description='Duo date of the task')
    priority: TaskPriorityEnumSchema = Field(description='Priority of the task')
    status: TaskStatusEnumSchema = Field(description='Status of the task', )


class TaskCreateSchemaRequest(TaskBaseSchema):
    pass


class TaskUpdateSchemaRequest(TaskBaseSchema):
    pass



class TaskSchemaResponse(TaskBaseSchema):
    id: int = Field(..., description="Id of the task")
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_data_model(cls, task: TaskDataModel):
        if task.id is None:
            raise ValueError(
                "Cannot create task from non-persisted entity: missing id. "
            )
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            priority=TaskPriorityEnumSchema[task.priority.name],
            status=TaskStatusEnumSchema[task.status.name]
        )


class TaskListResponseSchema(BaseModel):
    total_count: int
    tasks: list[TaskSchemaResponse] = []

    @classmethod
    def from_data_model(cls, data):
        return cls(
            total_count=data.total_count,
            tasks=[
                TaskSchemaResponse.from_data_model(task)
                for task in data.tasks
            ]
        )
