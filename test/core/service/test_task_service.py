import datetime
from unittest.mock import MagicMock

import pytest
from src.core.exceptions.service_exceptions import TaskNotFoundError
from src.core.service_contract.enum.task_enum import TaskStatusEnum
from src.core.service_contract.enum.task_priority_enum import TaskPriorityEnum
from src.core.services.task_service import TaskService
from src.infrastructure.models.task_model import TaskModel
from src.infrastructure.models.user_model import UserModel


class TestTaskService:
    @staticmethod
    @pytest.fixture
    def mock_task():
        user = UserModel(
            id=1,
            username='adelay',
            password='@1234',
            phone_number='09121111111',
            email='email@examples.com'
        )
        return TaskModel(
            id=1,
            user_id=user.id,
            title='Do test work.',
            description='Just lovely python.',
            due_date=datetime.datetime(2026, 4, 17),
            priority=1,
            status=1,
        )

    def test_when_find_by_id_except_call_get_model_by_id(self, mock_task):
        repository_mock = MagicMock()
        repository_mock.get_model_by_id.return_value = mock_task

        service = TaskService(repository_mock)
        service.find(user_id=1, task_id=1)
        repository_mock.get_model_by_id.assert_called_once()

    def test_when_find_by_id_return_data_model(self, mock_task):
        repository_mock = MagicMock()
        repository_mock.get_model_by_id.return_value = mock_task

        service = TaskService(repository_mock)
        data_model = service.find(user_id=1, task_id=1)

        assert data_model.id==1
        assert data_model.title=="Do test work."
        assert data_model.description=='Just lovely python.'
        assert data_model.priority==TaskPriorityEnum.MEDIUM
        assert data_model.status==TaskStatusEnum.IN_PROGRESS
        assert data_model.due_date==datetime.datetime(2026, 4, 17)

    def test_when_find_by_id_not_exist_return(self):
        repository_mock = MagicMock()
        repository_mock.get_model_by_id.return_value = None
        service = TaskService(repository_mock)

        with pytest.raises(TaskNotFoundError):
            service.find(user_id=1, task_id=1)

    def test_when_soft_delete_successfully_is_deleted_field_equal_true_and_deleted_at_is_not_none(self, mock_task):
        repository_mock = MagicMock()
        repository_mock.get_model_by_id.return_value = mock_task

        service = TaskService(repository_mock)
        service.soft_delete(user_id=1, task_id=1)
        assert mock_task.is_deleted is True
        assert mock_task.deleted_at is not None

    def test_when_get_list_by_filter_return_data_models_list(self, mock_task):
        repository_mock = MagicMock()
        repository_mock.get_list_by_filter.return_value = [mock_task], 1
        service = TaskService(repository_mock)
        tasks_data_model = service.get_all(user_id=1, page_number=1, page_size=10, status=TaskStatusEnum.IN_PROGRESS,
            priority=TaskPriorityEnum.MEDIUM)

        assert tasks_data_model.total_count==1
        assert tasks_data_model.tasks[0].id==1
        assert tasks_data_model.tasks[0].title=="Do test work."
        assert tasks_data_model.tasks[0].description=='Just lovely python.'

    def test_when_get_list_by_filter_return_empty(self):
        repository_mock = MagicMock()
        repository_mock.get_list_by_filter.return_value = [], 0
        service = TaskService(repository_mock)
        tasks_data_model = service.get_all(user_id=2, page_number=1, page_size=10, status=TaskStatusEnum.IN_PROGRESS,
            priority=TaskPriorityEnum.MEDIUM)
        assert tasks_data_model.total_count==0
        assert tasks_data_model.tasks==[]

    def test_when_add_return_data_model(self, mock_task):
        repository_mock = MagicMock()
        repository_mock.add.return_value = mock_task
        service = TaskService(repository_mock)
        data_model = service.add(user_id=1, title='Do test work.', description='Just lovely python.',
            due_date=datetime.datetime(2026, 4, 17), status=TaskStatusEnum.IN_PROGRESS,
            priority=TaskPriorityEnum.MEDIUM)
        assert data_model.id==1
        assert data_model.title=="Do test work."
        assert data_model.description=='Just lovely python.'
        assert data_model.priority==TaskPriorityEnum.MEDIUM
        assert data_model.status==TaskStatusEnum.IN_PROGRESS
        assert data_model.due_date==datetime.datetime(2026, 4, 17)

    def test_when_update_task_id_not_found_raise_task_not_found_error(self):
        repository_mock = MagicMock()
        repository_mock.get_model_by_id.return_value = None
        service = TaskService(repository_mock)
        with pytest.raises(TaskNotFoundError):
            service.update(
                user_id=1,
                task_id=2,
                title="Do Exercise",
                description="Ballet fit",
                due_date=datetime.datetime(2026, 6, 17),
                priority=TaskPriorityEnum.LOW,
                status=TaskStatusEnum.IN_PROGRESS,
            )

    def test_when_update_return_date_model(self, mock_task):
        repository_mock = MagicMock()
        repository_mock.get_model_by_id.return_value = mock_task
        mock_task.title = 'Do Exersice'
        mock_task.description = 'Ballet fit'
        repository_mock.update.return_value = mock_task
        service = TaskService(repository_mock)
        data_model = service.update(user_id=1, task_id=1, title='Do Exersice', description='Ballet fit',
            due_date=datetime.datetime(2026, 6, 17), priority=TaskPriorityEnum.MEDIUM,
            status=TaskStatusEnum.COMPLETED)
        assert data_model.id==1
        assert data_model.title=='Do Exersice'
        assert data_model.description=='Ballet fit'
        assert data_model.due_date==datetime.datetime(2026, 6, 17)
        assert data_model.priority==TaskPriorityEnum.MEDIUM
        assert data_model.status==TaskStatusEnum.COMPLETED


