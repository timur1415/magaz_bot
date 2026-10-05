import uuid

from fastapi import APIRouter, Request, Response

router = APIRouter(
    tags=["cart_middleware"])

@router.get('/api/cart/get-uuid')
async def cart_session_middleware(request: Request, response: Response):
    cart_uuid = request.cookies.get("cart_uuid")
    if not cart_uuid:
        cart_uuid = str(uuid.uuid4())
        response.set_cookie(key="cart_uuid", value=cart_uuid, max_age=60*60*24*7, httponly=True, samesite='lax')
    return {'cart_id': cart_uuid}