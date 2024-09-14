from pydantic import BaseModel


# Pydantic usage ensures type and nullish the DTO (DataTransferObject)
class UpdateCartItemDTO(BaseModel):
    itemId: str
    quantity: int
