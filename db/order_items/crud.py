from db.order_items.models import OrderItem
from db.order_items.shema import OrderItemCreate, OrderItemGet
from sqlalchemy.ext.asyncio import AsyncSession


async def create_order_item(session: AsyncSession, data: OrderItemCreate):
    order_item = OrderItem(**data.dict())
    session.add(order_item)
    await session.commit()
    await session.refresh(order_item)
    return order_item

async def order_item_get(session: AsyncSession, order_item: OrderItem, data: OrderItemGet):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(order_item, field, value)
    session.add(order_item)
    await session.commit()
    await session.refresh(order_item)
    return order_item


