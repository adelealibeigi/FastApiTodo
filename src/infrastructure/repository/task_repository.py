from datetime import datetime
from typing import Union

from injector import inject

from src.core.service_contract.interface.repository.itask_repository import ITaskRepository
from src.infrastructure.database.ipostgresql_connection import IPostgreSQLConnection
from src.infrastructure.models import TaskModel


class TaskRepository(ITaskRepository):
    @inject
    def __init__(self, database_connection: IPostgreSQLConnection) -> None:
        self.__database_connection: IPostgreSQLConnection = database_connection

    def get_model_by_id(self, user_id: int, task_id: int, is_deleted: bool = False) -> Union[TaskModel, None]:
        with self.__database_connection.get_session() as session:
            return (session.query(TaskModel)
                    .filter(TaskModel.id==task_id,
                            TaskModel.user_id==user_id,
                            TaskModel.is_deleted==is_deleted)
                    .one_or_none())

    def get_list_by_filter(self, user_id: int, page_number: int, page_size: int, status: int,
                           priority: int) -> tuple[list[TaskModel], int]:
        with self.__database_connection.get_session() as session:
            query = session.query(TaskModel).filter(TaskModel.user_id==user_id, TaskModel.is_deleted==False)
            if status is not None:
                query = query.filter(TaskModel.status==status)
            if priority is not None:
                query = query.filter(TaskModel.priority==priority)

            query = query.offset((page_number - 1) * page_size).limit(page_size)
            return query.all(), query.count()

    def update(self, model: TaskModel) -> TaskModel:
        with self.__database_connection.get_session() as session:
            task = session.query(TaskModel).filter(TaskModel.id==model.id).one()

            task.title = model.title
            task.description = model.description
            task.status = model.status
            task.priority = model.priority
            task.due_date = model.due_date

            session.commit()
            return task

    def add(self, model: TaskModel) -> TaskModel:
        with self.__database_connection.get_session() as session:
            session.add(model)
            session.commit()
            return model

    def set_soft_delete_status(self, model: TaskModel) -> None:
        with self.__database_connection.get_session() as session:
            (session.query(TaskModel).filter(TaskModel.id==model.id)
             .update({TaskModel.is_deleted: model.is_deleted,
                      TaskModel.deleted_at: model.deleted_at}))
            session.commit()

    def hard_delete(self, before_date: datetime) -> int:
        with self.__database_connection.get_session() as session:
            count = session.query(TaskModel).filter(
                TaskModel.is_deleted.is_(True),
                TaskModel.deleted_at <= before_date
            ).delete(synchronize_session=False)

            session.commit()
            return count

    def get_list(self, user_id: int, is_deleted: bool = False) -> tuple[list[TaskModel], int]:
        with self.__database_connection.get_session() as session:
            query = session.query(TaskModel).filter(TaskModel.user_id==user_id, TaskModel.is_deleted==is_deleted)
            return query.all(), query.count()
