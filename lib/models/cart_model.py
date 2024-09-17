from .cart_item_model import Item
from pydantic import BaseModel, Field
from bson import ObjectId


class CartItem(Item):
    quantity: int


class Cart(BaseModel):
    """The Cart class. Belongs to a user."""

    id: str = Field(alias="_id")
    items: list[CartItem]

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
