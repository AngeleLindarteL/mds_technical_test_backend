from pydantic import BaseModel
from lib.models.cart_item_model import ItemType


# Pydantic usage ensures type and nullish the DTO (DataTransferObject)
class UpdateCartItemDTO(BaseModel):
    itemId: str
    quantity: int


class AddItemToCartDTO(BaseModel):
    itemId: str


class CartDetailItem(BaseModel):
    name: str
    type: ItemType
    quantity: int
    unit_price: float
    sub_total: float


class CartTotals(BaseModel):
    total: float
    items: int
    detail: list[CartDetailItem] | None
