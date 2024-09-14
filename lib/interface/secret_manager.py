from abc import abstractmethod, ABCMeta
from typing import Any, Optional
from dataclasses import dataclass


class ISecretManager(metaclass=ABCMeta):
    """Common Secret Manager Interface for using secrets like credentials securely in all the app"""

    @abstractmethod
    def get(self, key: str, default_value: str) -> str:
        raise NotImplementedError("Implement get operation")
