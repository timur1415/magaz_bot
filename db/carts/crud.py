from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.carts.model import Cart
from db.carts.schema import CartCreate, CartUpdate

async def cart_create(session: AsyncSession, data: CartCreate):
    cart = Cart(**data.dict())
    session.add(cart)
    await session.commit()
    await session.refresh(cart)
    return cart

async def cart_get(session: AsyncSession, cart: Cart, data: CartUpdate):
    

