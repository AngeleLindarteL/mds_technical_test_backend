from lib.secrets.env_secret_manager import EnvSecretManager
from lib.interface.secret_manager import ISecretManager
from lib.enums.database import DatabaseCollections
from lib.models.cart_item_model import Item
from lib.database.mongo import MongoDatabase
from lib.interface.database import IDatabase, UpdateQuery
from lib.models.cart_model import Cart, CartItem
from lib.dtos.cart_dto import CartTotals, CartDetailItem, UpdateCartItemDTO
from lib.constants.errors import cart_errors

from fastapi import HTTPException
from bson import ObjectId
import pydash


class CartApiService:
    __items_repo__: IDatabase[Item]
    __cart_repo__: IDatabase[Cart]

    def __init__(self) -> None:
        sm: ISecretManager = EnvSecretManager()
        self.__items_repo__ = MongoDatabase(
            Item, sm, "mds-store", DatabaseCollections.ItemsCollection
        )
        self.__cart_repo__ = MongoDatabase(
            Cart, sm, "mds-store", DatabaseCollections.CartCollection
        )

    async def create_new_cart(self) -> Cart:
        new_cart = Cart(
            items=[],
            _id=str(ObjectId()),
        )

        return self.__cart_repo__.save(new_cart)

    async def get_cart_totals(self, cart_id: str) -> Cart:
        cart = self.__get__cart__(cart_id)

        details: list[CartDetailItem] = []
        total_value = 0

        for item in cart.items:
            subtotal = item.price * item.quantity
            total_value += subtotal

            details.append(
                CartDetailItem(
                    name=item.name,
                    quantity=item.quantity,
                    sub_total=subtotal,
                    type=item.type,
                    unit_price=item.price,
                )
            )

        return CartTotals(detail=details, items=len(cart.items), total=total_value)

    async def add_item_to_cart(self, cart_id: str, item_id: str) -> Cart:
        item_to_add = self.__get__item__(item_id)
        cart = self.__get__cart__(cart_id)

        units_to_append = 1
        item_in_cart = pydash.find(cart.items, lambda it: it.id == item_to_add.id)

        if item_in_cart is not None:
            cart.items = self.__remove_cart_item__(cart.items, item_to_add.id)
            units_to_append += item_in_cart.quantity

        if units_to_append > item_to_add.stock:
            raise HTTPException(
                status_code=400,
                detail=cart_errors["NoStock"],
            )

        cart.items.append(
            CartItem(
                **item_to_add.model_dump(by_alias=True),
                quantity=units_to_append,
            ),
        )

        return self.__cart_repo__.updateOne(
            UpdateQuery(
                filter={"_id": cart.id},
                update={"$set": {**cart.model_dump(by_alias=True)}},
            )
        )

    async def update_cart_item(self, cart_id: str, update: UpdateCartItemDTO) -> Cart:
        item_to_add = self.__get__item__(update.itemId)
        cart = self.__get__cart__(cart_id)

        item_in_cart = pydash.find(cart.items, lambda it: it.id == item_to_add.id)

        if item_in_cart is None:
            raise HTTPException(
                status_code=400,
                detail=cart_errors["ItemNotInCart"],
            )

        if update.quantity > item_to_add.stock:
            raise HTTPException(
                status_code=400,
                detail=cart_errors["NoStock"],
            )

        if update.quantity == 0:
            return await self.delete_cart_item(cart_id, update.itemId)

        cart.items = self.__remove_cart_item__(cart.items, update.itemId)

        item_to_append = CartItem(
            **item_to_add.model_dump(by_alias=True),
            quantity=update.quantity,
        ).model_dump(by_alias=True)

        cart.items.append(item_to_append)

        return self.__cart_repo__.updateOne(
            UpdateQuery(
                filter={"_id": cart.id},
                update={"$set": {**cart.model_dump(by_alias=True)}},
            )
        )

    async def delete_cart_item(self, cart_id: str, item_id: str) -> Cart:
        cart = self.__get__cart__(cart_id)
        cart.items = self.__remove_cart_item__(cart.items, item_id)

        return self.__cart_repo__.updateOne(
            UpdateQuery(
                filter={"_id": cart.id},
                update={"$set": {**cart.model_dump(by_alias=True)}},
            )
        )

    def __remove_cart_item__(
        self, items: list[CartItem], item_to_remove: str
    ) -> list[CartItem]:
        return list(filter(lambda it: it.id != item_to_remove, items))

    def __get__item__(self, item_id) -> Item:
        item = self.__items_repo__.findByUnique({"_id": item_id})

        if item is None:
            raise HTTPException(
                status_code=400,
                detail=cart_errors["ItemNotFound"],
            )

        return item

    def __get__cart__(self, cart_id) -> Cart:
        cart = self.__cart_repo__.findByUnique({"_id": cart_id})

        if cart is None:
            raise HTTPException(
                status_code=404,
                detail=cart_errors["CartNotFound"],
            )

        return cart
