from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Generic
import mongomock

from lib.utils.singleton import SingletonBase
from lib.interface.database import IDatabase, FindQuery, UpdateQuery, ModelType
from lib.interface.secret_manager import ISecretManager
from lib.constants.database import DEFAULT_MONGO_URI
from lib.enums.database import DatabaseCollections


class MongoDatabase(SingletonBase, IDatabase):
    __client__: MongoClient
    __db__: Database
    __coll__: Collection
    __entity__: Generic[ModelType]

    def _initialize(
        self,
        entity: Generic[ModelType],
        sm: ISecretManager,
        db_name: str,
        collection: DatabaseCollections,
        use_mock=False,
    ) -> None:
        """Uses dependency injection + singleton to be resource efficient"""
        uri = sm.get(
            "mongo_connection_string",
            DEFAULT_MONGO_URI,
        )

        if use_mock:
            self.__client__ = mongomock.MongoClient()
        else:
            self.__client__ = MongoClient(uri)

        self.__db__ = self.__client__[db_name]
        self.__coll__ = self.__db__[collection.value]
        self.__entity__ = entity

    def findByUnique(self, query: dict) -> ModelType | None:
        result = self.__coll__.find_one(query)

        if result is not None:
            return self.__entity__(**result)

        return None

    def find(self, query: FindQuery) -> list[ModelType]:
        m_query = self.__coll__.find(query.filter)
        results: list[ModelType] = []

        if query.take is not None:
            m_query.limit(query.take)

        if query.skip is not None:
            m_query.skip(query.skip)

        for x in m_query:
            results.append(self.__entity__(**x))

        return results

    def updateOne(self, query: UpdateQuery) -> ModelType | None:
        self.__coll__.update_one(query.filter, query.update)

        return self.findByUnique(query.filter)

    def save(self, obj: ModelType) -> ModelType:
        self.__coll__.insert_one(obj.model_dump(by_alias=True))

        return obj
