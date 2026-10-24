import uuid

from fastapi import APIRouter, Form, Request

from db.cart_items.crud import get_all_items_by_id
from db.carts.crud import get_or_create_cart_by_anonymous_id
from db.order_items.crud import create_order_item
from db.orders.crud import create_order
from server.deps import SessionDep

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("")
async def create_order(
    request: Request,
    session: SessionDep,
    name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
):
    cart_uuid = request.cookies.get("cart_uuid")
    print(f'cart_uuid: {cart_uuid}, name: {name}, phone: {phone}, address: {address}')
    cart = await get_or_create_cart_by_anonymous_id(session, uuid.UUID(cart_uuid))
    rows = await get_all_items_by_id(session, cart.id)
    order = await create_order(session, cart.id, name, phone, address)
    for row in rows:
        await create_order_item(
            session,
            order.id,
            row.product_id,
            row.quantity,
        )








