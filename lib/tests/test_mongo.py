from lib.interface.database import FindQuery, UpdateQuery
from lib.enums.database import DatabaseCollections
from lib.secrets.env_secret_manager import EnvSecretManager
from lib.models.base_item_model import BaseItem, ItemType
from lib.secrets.env_secret_manager import EnvSecretManager
from lib.database.mongo import MongoDatabase

from bson import ObjectId

sm = EnvSecretManager()


def test_singleton_connection() -> None:
    """Test that connection with same params is a real singleton"""

    db1 = MongoDatabase(
        BaseItem, sm, "mds-store", DatabaseCollections.CartCollection, True
    )
    db2 = MongoDatabase(
        BaseItem, sm, "mds-store", DatabaseCollections.CartCollection, True
    )

    assert db1 is db2


def test_inserting_one_registry() -> None:
    """Test inserting one registry"""
    db = MongoDatabase(
        BaseItem, sm, "mds-store", DatabaseCollections.CartCollection, True
    )

    item_to_save = BaseItem(
        _id=str(ObjectId()),
        name="Rizador de pelo :3",
        stock=10,
        price=99.99,
        type=ItemType.PRODUCT,
    )

    it = db.save(item_to_save)
    assert it.id == item_to_save.id


def test_inserting_one_and_find_it() -> None:
    """Test inserting one registry"""
    db = MongoDatabase(
        BaseItem, sm, "mds-store", DatabaseCollections.CartCollection, True
    )

    item_to_save = BaseItem(
        _id=str(ObjectId()),
        name="Rizador de pelo :3",
        stock=10,
        price=99.99,
        type=ItemType.PRODUCT,
    )

    it = db.save(item_to_save)
    reg = db.findByUnique({"_id": it.id})

    assert reg is not None
