from fastapi.exceptions import RequestValidationError
from injector import Injector
from src.injection import Injection
from fastapi_swagger import patch_fastapi
from fastapi import FastAPI
from src.core.exceptions.service_exceptions import ServiceError
from src.service_api.exception.exception_handler import generic_exception_handler, service_error_handler, \
    validation_error_handler
from fastapi_injector import attach_injector
from src.service_api.routers.auth_router import auth_router
from src.service_api.routers.task_router import task_router
from dataclasses import dataclass


@dataclass
class ServeApi:
    injector: Injector

    def create_app(self) -> FastAPI:
        app = FastAPI(
            docs_url=None,
            swagger_ui_oauth2_redirect_url=None,
            openapi_tags=self._tags_metadata(),
            title="Simple Todo App API",
            description="Todo application with Clean Architecture",
            version="1.0.0",
            contact={
                "name": "Adele Alibeigi",
                "email": "adelealibeigi@gmail.com",
            },
            license_info={"name": "MIT"},
        )

        self._configure_docs(app)
        self._configure_exception_handlers(app)
        self._configure_dependency_injection(app)
        self._configure_routers(app)

        return app

    @staticmethod
    def _configure_docs(app: FastAPI) -> None:
        patch_fastapi(app, docs_url="/swagger")

    @staticmethod
    def _configure_exception_handlers(app: FastAPI) -> None:
        app.add_exception_handler(ServiceError, service_error_handler)  # type: ignore[arg-type]
        app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]
        app.add_exception_handler(Exception, generic_exception_handler)

    def _configure_dependency_injection(self, app: FastAPI) -> None:
        attach_injector(app, self.injector)

    @staticmethod
    def _configure_routers(app: FastAPI) -> None:
        app.include_router(task_router)
        app.include_router(auth_router)

    @staticmethod
    def _tags_metadata() -> list[dict]:
        return [
            {
                "name": "task",
                "description": "Task management operations",
            },
            {
                "name": "auth",
                "description": "Authentication operations",
            },
        ]



