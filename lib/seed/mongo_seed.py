from faker import Faker
from bson import ObjectId

from lib.interface.database import IDatabase
from lib.models.cart_item_model import Item, ItemType
from lib.models.cart_item_model import Item
from lib.database.mongo import MongoDatabase
from lib.secrets.env_secret_manager import EnvSecretManager
from lib.interface.secret_manager import ISecretManager
from lib.enums.database import DatabaseCollections

fake = Faker()


def seed_items(db: IDatabase) -> None:
    for _ in range(100):
        print("Seeding item")
        item_to_save = Item(
            name=fake.name(),
            stock=fake.random_digit(),
            price=fake.pydecimal(2, 1, True),
            meta={
                "address": fake.address(),
            },
            type=fake.enum(ItemType),
            _id=str(ObjectId()),
        )

        db.save(item_to_save)
        print("Seed one Ok!")

    print("Finish seeding")


if __name__ == "__main__":
    sm: ISecretManager = EnvSecretManager()
    items_repo = MongoDatabase(
        Item, sm, "mds-store", DatabaseCollections.ItemsCollection
    )

    seed_items(items_repo)
