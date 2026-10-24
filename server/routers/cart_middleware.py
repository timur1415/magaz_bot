import uuid

from fastapi import APIRouter, Request, Response

from db.cart_items.crud import cart_item_create
from db.carts.crud import delite_cart, get_or_create_cart_by_anonymous_id
from db.carts.schema import DeliteCart
from server.deps import SessionDep

router = APIRouter(
    tags=["cart_middleware"])

@router.get('/api/cart/get-uuid')
async def cart_session_middleware(request: Request, response: Response):
    cart_uuid = request.cookies.get("cart_uuid")
    if not cart_uuid:
        cart_uuid = str(uuid.uuid4())
        response.set_cookie(key="cart_uuid", value=cart_uuid, max_age=60*60*24*7, httponly=True, samesite='lax')
    return {'cart_id': cart_uuid}



@router.post('/api/carts/add/{product_id}')
async def add_to_cart(
    product_id: int,
    session: SessionDep,
    request: Request,
    response: Response,
):
    cart_uuid = request.cookies.get("cart_uuid")
    
    if not cart_uuid:
        return {"error": "cart_uuid not found"}

    cart = await get_or_create_cart_by_anonymous_id(session, uuid.UUID(cart_uuid))
    print(f'cart {cart} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    item = await cart_item_create(
        session,
        cart.id,
        product_id,
    )
    print(f'item {item.quantity} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    return {"status": "success", }

@router.post('/api/carts/delete')
async def delete_cart(
    session: SessionDep,
    request: Request,
):
    cart_uuid = request.cookies.get("cart_uuid")
    if not cart_uuid:
        return {"error": "cart_uuid not found"}


    data = DeliteCart(
        anonymous_id=uuid.UUID(cart_uuid)
    )
    cart = await delite_cart(session, data)
    if not cart:
        return {"error": "cart not found"}
    return {"status": "success"}