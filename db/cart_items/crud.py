from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.cart_items.model import CartItem
from db.products.model import Product


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

async def get_all_item(session: AsyncSession):
    result = await session.execute(select(CartItem))
    items = result.scalars().all()
    return items

async def get_all_items_by_id(session: AsyncSession, cart_id: int):
    
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
        .where(CartItem.cart_id == cart_id)
    )

    rows = result.all()
    return rows




    