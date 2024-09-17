from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Any


class ItemType(Enum):
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"


class Item(BaseModel):
    """The Item class contains the properties that all cart items share between them."""

    id: str = Field(alias="_id")
    name: str
    type: ItemType
    price: float
    stock: int
    # This meta field enables all the cart items having another different properties but using a shared model.
    # This any can be replaced by a union type of EventItemMeta and ProductItemMeta. But the docs doesn't specify what properties are different between this type of items.
    meta: dict[str, Any]

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
