from fastapi import APIRouter, Query, Depends, Path
from fastapi_injector import Injected
from starlette import status

from src.core.service_contract.data_model.task_data_model import TasksDataModel, TaskDataModel
from src.core.service_contract.data_model.user_data_model import UserDataModel
from src.core.service_contract.enum.task_enum import TaskStatusEnum
from src.core.service_contract.enum.task_priority_enum import TaskPriorityEnum

from src.core.service_contract.interface.itask_service import ITaskService
from src.service_api.dependency.auth import get_current_user
from src.service_api.schemas.task_schema import TaskFilterSchema, TaskListResponseSchema, TaskCreateSchemaRequest, \
    TaskSchemaResponse, TaskUpdateSchemaRequest


task_router = APIRouter(prefix="/task", tags=["task"])


@task_router.get('/detail/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskSchemaResponse)
def get(task_id: int = Path(..., gt=0), user: UserDataModel = Depends(get_current_user),
        task_service: ITaskService = Injected(ITaskService)):
    task: TaskDataModel = task_service.find(user_id=user.id, task_id=task_id)
    return TaskSchemaResponse.from_data_model(task)


@task_router.get("/list", status_code=status.HTTP_200_OK, response_model=TaskListResponseSchema)
def tasks_list(

        page_number: int = Query(1, ge=1, alias="offset",
            description="Page number starting from 1 (1 = first page)."),
        page_size: int = Query(10, ge=1, le=50, alias="limit",
            description="Number of items per page (max 100)."),
        task_filters: TaskFilterSchema = Depends(TaskFilterSchema),
        user: UserDataModel = Depends(get_current_user),
        task_service: ITaskService = Injected(ITaskService)):
    priority = TaskPriorityEnum[task_filters.priority.value] if task_filters.priority is not None else None
    status = TaskStatusEnum[task_filters.status.value] if task_filters.status is not None else None

    tasks_data: TasksDataModel = task_service.get_all(user_id=user.id, page_size=page_size, page_number=page_number,
        status=status, priority=priority)
    return TaskListResponseSchema.from_data_model(tasks_data)


@task_router.post("/create", status_code=status.HTTP_200_OK, response_model=TaskSchemaResponse)
def create_task(request: TaskCreateSchemaRequest, user: UserDataModel = Depends(get_current_user),
                task_service: ITaskService = Injected(ITaskService)):
    task = task_service.add(user_id=user.id, title=request.title, description=request.description,
        due_date=request.due_date, priority=TaskPriorityEnum[request.priority.value],
        status=TaskStatusEnum[request.status.value])
    return TaskSchemaResponse.from_data_model(task)


@task_router.post("/update/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskSchemaResponse)
def update_task(request: TaskUpdateSchemaRequest, task_id: int = Path(..., gt=0),
                user: UserDataModel = Depends(get_current_user),
                task_service: ITaskService = Injected(ITaskService)):
    task = task_service.update(user_id=user.id, task_id=task_id, title=request.title,
        description=request.description, due_date=request.due_date, priority=TaskPriorityEnum[request.priority.value],
        status=TaskStatusEnum[request.status.value])
    return TaskSchemaResponse.from_data_model(task)


@task_router.post('/activate-deleted-task/{task_id}', status_code=status.HTTP_200_OK)
def active_deleted_task(task_id: int = Path(..., gt=0), user: UserDataModel = Depends(get_current_user),
                task_service: ITaskService = Injected(ITaskService)):
    task_service.active_deleted_task(user_id=user.id, task_id=task_id)


@task_router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int = Path(..., gt=0), user: UserDataModel = Depends(get_current_user),
                task_service: ITaskService = Injected(ITaskService)):
    task_service.soft_delete(user_id=user.id, task_id=task_id)


@task_router.get("/deleted-list", status_code=status.HTTP_200_OK, response_model=TaskListResponseSchema)
def deleted_list(user: UserDataModel = Depends(get_current_user),
                 task_service: ITaskService = Injected(ITaskService)):
    tasks_data: TasksDataModel = task_service.get_deleted_list(user_id=user.id)
    return TaskListResponseSchema.from_data_model(tasks_data)
