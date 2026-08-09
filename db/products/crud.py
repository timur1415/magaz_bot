from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.products.model import Product
from db.products.schema import ProductCreate
from db.products.schema import ProductUpdate

async def get_all(session: AsyncSession):
    cursor = await session.execute(select(Product))
    return cursor.scalars().all()

async def create(session: AsyncSession, data: ProductCreate):
    product = Product(**data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product

async def get_by_id(session: AsyncSession, product_id: int):
    cursor = await session.execute(select(Product).where(Product.id == product_id))
    return cursor.scalars().first()

async def update(session: AsyncSession, product_id: int, data: ProductUpdate):
    product = await get_by_id(session, product_id)
    if product:
        for key, value in data.model_dump().items():
            setattr(product, key, value)
        await session.commit()
        await session.refresh(product)
    return product

async def delete(session: AsyncSession, product_id: int):
    product = await get_by_id(session, product_id)
    if product:
        await session.delete(product)
        await session.commit()
    return product