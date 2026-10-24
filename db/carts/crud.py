from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.cart_items.model import CartItem
from db.carts.model import Cart
from db.carts.schema import CartCreate, GetCart, DeliteCart


async def cart_create(session: AsyncSession, data: CartCreate):
    cart = Cart(**data.dict())
    session.add(cart)
    await session.commit()
    await session.refresh(cart)
    return cart

async def cart_get(session: AsyncSession, cart: Cart, data: GetCart):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(cart, field, value)
    session.add(cart)
    await session.commit()
    await session.refresh(cart)
    return cart


async def get_or_create_cart_by_anonymous_id(session: AsyncSession, anonymous_id):
    result = await session.execute(
        select(Cart).where(Cart.anonymous_id == anonymous_id)
    )
    cart = result.scalars().first()
    if not cart:
        cart = Cart(anonymous_id=anonymous_id)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)
    return cart

async def delite_cart(session: AsyncSession, data: DeliteCart):
    result = await session.execute(
        select(Cart).where(Cart.anonymous_id == data.anonymous_id)
    )
    cart = result.scalars().first()
    if cart:
        await session.execute(delete(CartItem).where(CartItem.cart_id == cart.id))
        await session.delete(cart)
        await session.commit()
    return cart



