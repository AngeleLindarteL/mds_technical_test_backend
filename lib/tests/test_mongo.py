from lib.interface.database import FindQuery, UpdateQuery
from lib.enums.database import DatabaseCollections
from lib.secrets.env_secret_manager import EnvSecretManager
from lib.models.cart_item_model import Item, ItemType
from lib.secrets.env_secret_manager import EnvSecretManager
from lib.database.mongo import MongoDatabase

from bson import ObjectId

sm = EnvSecretManager()


def test_singleton_connection() -> None:
    """Test that connection with same params is a real singleton"""

    db1 = MongoDatabase(Item, sm, "mds-store", DatabaseCollections.ItemsCollection)
    db2 = MongoDatabase(Item, sm, "mds-store", DatabaseCollections.ItemsCollection)

    assert db1 is db2


def test_inserting_one_registry() -> None:
    """Test inserting one registry"""
    db = MongoDatabase(Item, sm, "mds-store", DatabaseCollections.ItemsCollection)

    item_to_save = Item(
        _id=str(ObjectId()),
        name="Rizador de pelo",
        stock=10,
        price=99.99,
        type=ItemType.PRODUCT,
        meta={},
    )

    it = db.save(item_to_save)
    assert it.id == item_to_save.id


def test_inserting_one_and_find_it() -> None:
    """Test inserting one registry and finding it with findByUnique"""
    db = MongoDatabase(Item, sm, "mds-store", DatabaseCollections.ItemsCollection)

    item_to_save = Item(
        _id=str(ObjectId()),
        name="Rizador de pelo",
        stock=10,
        price=99.99,
        type=ItemType.PRODUCT,
        meta={},
    )

    it = db.save(item_to_save)
    reg = db.findByUnique({"_id": it.id})

    assert reg is not None


def test_find() -> None:
    """Test basic find"""
    db = MongoDatabase(Item, sm, "mds-store", DatabaseCollections.ItemsCollection)

    registries = db.find(
        FindQuery(
            filter={},
            skip=0,
            take=10,
        )
    )

    assert registries is not None
    assert len(registries) != 0


def test_update_one() -> None:
    """Test update one registry"""
    db = MongoDatabase(Item, sm, "mds-store", DatabaseCollections.ItemsCollection)

    og_name = "Rizador de pelo"
    up_name = "Rizador de pelo Modificado :)"

    item_to_save = Item(
        _id=str(ObjectId()),
        name=og_name,
        stock=10,
        price=99.99,
        type=ItemType.PRODUCT,
        meta={},
    )

    it = db.save(item_to_save)
    db.updateOne(UpdateQuery(filter={"_id": it.id}, update={"$set": {"name": up_name}}))
    latest_reg = db.findByUnique({"_id": it.id})

    assert it.name == og_name
    assert latest_reg.name == up_name
