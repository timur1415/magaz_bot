from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.cart_items.models import CartItem
from db.cart_items.shema import CartItemGet


async def cart_item_create(session: AsyncSession, cart_id: int, product_id: int):
    result = await session.execute(
        select(CartItem).where(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id,
        )
    )
    item = result.scalars().first()

    if item:
        item.quantity += 1
        await session.commit()
        await session.refresh(item)
        return item

    else:
        new_item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=1,
        )
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)
        return new_item

async def get_cart_item(session: AsyncSession, data: CartItemGet):
    result = await session.get(CartItem, data.id)
    
    return result




    