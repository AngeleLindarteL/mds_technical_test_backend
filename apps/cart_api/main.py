from fastapi import FastAPI, Depends
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .service import CartApiService
from lib.dtos.cart_dto import CartTotals, AddItemToCartDTO, UpdateCartItemDTO
from lib.models.cart_model import Cart

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/cart")


@router.post("/", response_model=Cart)
async def get_cart(service: CartApiService = Depends(CartApiService)):
    """Gets the totals and subtotal of the cart"""
    return await service.create_new_cart()


@router.get("/{id}", response_model=CartTotals)
async def get_cart(id: str, service: CartApiService = Depends(CartApiService)):
    """Gets the totals and subtotal of the cart"""
    return await service.get_cart_totals(id)


@router.post("/{id}")
async def add_item_to_cart(
    id: str, body: AddItemToCartDTO, service: CartApiService = Depends(CartApiService)
):
    """Adds an item to the cart :)"""
    return await service.add_item_to_cart(id, body.itemId)


@router.put("/{id}")
async def update_cart_item(
    id: str, body: UpdateCartItemDTO, service: CartApiService = Depends(CartApiService)
):
    """Updates an item of the cart :)"""
    return await service.update_cart_item(id, body)


@router.delete("/{id}/{item_id}")
async def delete_cart_item(
    id: str, item_id: str, service: CartApiService = Depends(CartApiService)
):
    """Deletes an item of the cart :)"""
    return await service.delete_cart_item(id, item_id)


app.include_router(router)
