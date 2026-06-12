from injector import Injector

from src.core.service_contract.interface.iauth_service import IAuthService
from src.core.service_contract.interface.ipassword_hasher import IPasswordHasher
from src.core.service_contract.interface.itask_service import ITaskService
from src.core.service_contract.interface.itoken_provider import ITokenProvider
from src.core.service_contract.interface.iuser_service import IUserService
from src.core.service_contract.interface.repository.itask_repository import ITaskRepository
from src.core.service_contract.interface.repository.iuser_repository import IUserRepository
from src.core.services.auth_service import AuthService
from src.core.services.task_service import TaskService
from src.core.services.user_service import UserService
from src.infrastructure.security.jwt_provider import TokenProvider
from src.infrastructure.security.password_hasher import PasswordHasher
from src.infrastructure.database.ipostgresql_connection import IPostgreSQLConnection
from src.infrastructure.database.postgresql_connection import PostgreSQLConnection
from src.infrastructure.repository.task_repository import TaskRepository
from src.infrastructure.repository.user_repository import UserRepository


class Injection:
    def get_injector(self):
        injector: Injector = Injector()
        self.__bind(injector)
        return injector

    @staticmethod
    def __bind(injector: Injector):
        injector.binder.bind(ITaskService, TaskService)
        injector.binder.bind(IUserService, UserService)
        injector.binder.bind(IAuthService, AuthService)
        injector.binder.bind(ITaskRepository, TaskRepository)
        injector.binder.bind(IUserRepository, UserRepository)
        injector.binder.bind(IPostgreSQLConnection, PostgreSQLConnection)
        injector.binder.bind(ITokenProvider, TokenProvider)
        injector.binder.bind(IPasswordHasher, PasswordHasher)

