from abc import abstractmethod, ABCMeta
from typing import Any, Optional, Generic, TypeVar
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class FindQuery:
    take: int
    filter: dict
    skip: Optional[int] = 0


@dataclass
class UpdateQuery:
    filter: dict
    update: dict


ModelType = TypeVar("ModelType", bound=BaseModel)


class IDatabase(Generic[ModelType], metaclass=ABCMeta):
    @abstractmethod
    def findByUnique(self, query: dict) -> ModelType | None:
        raise NotImplementedError("Implement find by unique operation")

    @abstractmethod
    def find(self, query: FindQuery) -> list[ModelType]:
        raise NotImplementedError("Implement find operation")

    @abstractmethod
    def updateOne(self, query: UpdateQuery) -> ModelType:
        raise NotImplementedError("Implement save operation")

    @abstractmethod
    def save(self, obj: ModelType) -> ModelType:
        raise NotImplementedError("Implement update operation")
