from unittest.mock import MagicMock

import pytest

from src.core.exceptions.service_exceptions import UserNotFoundError, InvalidCredentialsError

from src.core.services.auth_service import AuthService


class TestAuthService:
    @staticmethod
    @pytest.fixture
    def user_repository(): return MagicMock()

    @staticmethod
    @pytest.fixture
    def password_hasher(): return MagicMock()

    @staticmethod
    @pytest.fixture
    def token_provider(): return MagicMock()

    @staticmethod
    @pytest.fixture
    def auth_service(user_repository, password_hasher, token_provider):
        return AuthService(user_repository, password_hasher, token_provider)

    def test_login_should_fail_when_user_not_found_raise_user_not_found(self, auth_service, user_repository):
        user_repository.get_model_by_user_name.return_value = None
        with pytest.raises(UserNotFoundError):
            auth_service.login("testuser", "123456")

    def test_login_should_fail_when_password_is_invalid_raise_invalid_credentials_error(self, auth_service, user_repository, password_hasher,
                                                        token_provider):
        user_model = MagicMock()
        user_model.password = "hashed_password"
        user_repository.get_model_by_user_name.return_value = user_model
        password_hasher.verify_password.return_value = False
        with pytest.raises(InvalidCredentialsError):
            auth_service.login(username="testuser", password="wrong_password")

        user_repository.get_model_by_user_name.assert_called_once_with(username="testuser")
        password_hasher.verify_password.assert_called_once_with(
            plain_password="wrong_password",
            hashed="hashed_password"
        )
        token_provider.generate_access_token.assert_not_called()
        token_provider.generate_refresh_token.assert_not_called()

    def test_login_should_return_token_data_model_when_credentials_are_valid(self, auth_service, user_repository, password_hasher,
                                                                   token_provider):
        user_model = MagicMock()
        user_model.id = 1
        user_model.password = "hashed_password"
        user_repository.get_model_by_user_name.return_value = user_model
        password_hasher.verify_password.return_value = True
        token_provider.generate_access_token.return_value = "access-token"
        token_provider.generate_refresh_token.return_value = "refresh-token"
        token_data_model = auth_service.login(username="testuser", password="correct_password")

        assert token_data_model.access_token=="access-token"
        assert token_data_model.refresh_token=="refresh-token"

        user_repository.get_model_by_user_name.assert_called_once_with(username="testuser")
        password_hasher.verify_password.assert_called_once_with(
            plain_password="correct_password",
            hashed="hashed_password"
        )
        token_provider.generate_access_token.assert_called_once_with(user_id=1)
        token_provider.generate_refresh_token.assert_called_once_with(user_id=1)
