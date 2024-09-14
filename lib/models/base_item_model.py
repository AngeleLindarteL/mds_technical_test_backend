from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId


class ItemType(Enum):
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"


class BaseItem(BaseModel):
    """The BaseItem class contains the properties that all cart items share between them."""

    id: str = Field(alias="_id")
    name: str
    type: ItemType
    price: float
    stock: int

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
