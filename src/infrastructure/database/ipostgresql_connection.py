from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


class IPostgreSQLConnection(ABC):

    def __init__(self) -> None:
        self._engine: Engine
        self._session_factory: sessionmaker

    @abstractmethod
    def get_session(self):
        raise NotImplementedError
