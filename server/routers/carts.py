import uuid

from fastapi import APIRouter, Request
from sqlalchemy import select

from db.cart_items.model import CartItem
from db.carts.crud import get_or_create_cart_by_anonymous_id
from db.products.model import Product
from server.deps import SessionDep
from db.cart_items.crud import get_all_items_by_id

router = APIRouter(tags=["carts"])

@router.get("/api/cart")
async def get_cart(request: Request, session: SessionDep):
    cart_uuid = request.cookies.get("cart_uuid")

    if not cart_uuid:
        return []

    cart = await get_or_create_cart_by_anonymous_id(session, uuid.UUID(cart_uuid))

    

    rows = await get_all_items_by_id(session, cart.id)

    return [
        {
            "id": row.id,
            "product_id": row.product_id,
            "quantity": row.quantity,
            "name": row.name,
            "price": row.price,
            "photo": row.photo,
            "description": row.description,
        }
        for row in rows
    ]