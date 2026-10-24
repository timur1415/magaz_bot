from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.orders.model import Order
from db.orders.shema import OrderCreate, OrderGet

async def create_order(session: AsyncSession, data: OrderCreate):
    order = Order(**data.dict())
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order

async def order_get(session: AsyncSession, order: Order, data: OrderGet):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(order, field, value)
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order