import uuid

from fastapi import APIRouter, Request
from sqlalchemy import select

from db.cart_items.models import CartItem
from db.carts.crud import get_or_create_cart_by_anonymous_id
from db.products.model import Product
from server.deps import SessionDep

router = APIRouter(tags=["carts"])

@router.get("/api/cart")
async def get_cart(request: Request, session: SessionDep):
    cart_uuid = request.cookies.get("cart_uuid")

    if not cart_uuid:
        return []

    cart = await get_or_create_cart_by_anonymous_id(session, uuid.UUID(cart_uuid))

    result = await session.execute(
        select(
            CartItem.id,
            CartItem.product_id,
            CartItem.quantity,
            Product.name,
            Product.price,
            Product.photo,
            Product.description,
        )
        .join(Product, Product.id == CartItem.product_id)
        .where(CartItem.cart_id == cart.id)
    )

    rows = result.all()

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