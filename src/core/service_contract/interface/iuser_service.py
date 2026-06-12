from abc import ABC, abstractmethod


class IUserService(ABC):
    @abstractmethod
    def find(self, username: str):
        raise NotImplementedError

    # @abstractmethod
    # def add(self, username: str, password: str, phone_number: str, email: str):
    #     raise NotImplementedError
