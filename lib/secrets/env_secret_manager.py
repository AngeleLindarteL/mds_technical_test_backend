import os

from lib.interface.secret_manager import ISecretManager
from lib.utils.singleton import SingletonBase


# Using singleton here allows to use the secrets everywhere in the app just spawning a new class
# This secret manager uses the execution environment variables :).
class EnvSecretManager(ISecretManager, SingletonBase):
    variables: dict[str, str] = {}

    def _initialize(self) -> None:
        all_vars = dict(os.environ)

        for k, v in all_vars.items():
            normalized_key = k.strip().lower()
            self.variables[normalized_key] = v

    def get(self, key: str, default_value: str) -> str:
        normalized_key = key.strip().lower()

        return self.variables.get(normalized_key, default_value)
