from unittest.mock import MagicMock

import pytest

from src.core.exceptions.service_exceptions import UserNotFoundError
from src.core.services.user_service import UserService
from src.infrastructure.models.user_model import UserModel


class TestUserService:
    @staticmethod
    @pytest.fixture
    def mock_user():
        user = UserModel(
            id=1,
            username='adelay',
            password='@1234',
            phone_number='09121111111',
            email='email@examples.com'
        )
        return user

    def test_when_find_by_username_return_data_model(self, mock_user):
        repository_mock = MagicMock()
        repository_mock.get_model_by_user_name.return_value = mock_user
        service = UserService(repository_mock)
        user_data_model = service.find(username='adelay')
        assert user_data_model.id==1
        assert user_data_model.username=='adelay'
        assert user_data_model.phone_number=='09121111111'
        assert user_data_model.email=='email@examples.com'

    def test_when_find_by_username_not_exist_raise_user_not_found(self):
        repository_mock = MagicMock()
        repository_mock.get_model_by_user_name.return_value = None
        service = UserService(repository_mock)
        with pytest.raises(UserNotFoundError):
            service.find(username='sarah')


