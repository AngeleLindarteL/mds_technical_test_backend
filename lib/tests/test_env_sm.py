import os
from lib.secrets.env_secret_manager import EnvSecretManager


def test_getting_inexistent_key() -> None:
    """Test getting an inexistent key from env secret manager using empty string"""
    # Clear singleton instances first
    EnvSecretManager().clear_instance()

    assert EnvSecretManager().get("inexistent_key", "") == ""


def test_getting_existent_key() -> None:
    """Test getting an inexistent key from env secret manager"""
    # Clear singleton instances first
    EnvSecretManager().clear_instance()

    os.environ["HeLLo_WoRlD"] = "hello!"

    assert EnvSecretManager().get("hello_world", "") == "hello!"
