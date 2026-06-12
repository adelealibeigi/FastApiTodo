from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session

from src.core.exceptions.service_exceptions import DatabaseError
from src.infrastructure.config import settings
from src.infrastructure.database.ipostgresql_connection import IPostgreSQLConnection


class PostgreSQLConnection(IPostgreSQLConnection):
    def __init__(self) -> None:
        super().__init__()
        self._engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
        self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self._engine,
            expire_on_commit=False)

    @contextmanager
    def get_session(self):
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as exc:
            session.rollback()
            raise DatabaseError() from exc
        finally:
            session.close()
