from sqlalchemy.ext.asyncio import AsyncSession

from db.cart_items.models import CartItem
from db.cart_items.shema import CartItemCreate


async def cart_item_create(session: AsyncSession, data: CartItemCreate):
    cart_item = CartItem(**data.dict())
    session.add(cart_item)
    await session.commit()
    await session.refresh(cart_item)
    return cart_item




    