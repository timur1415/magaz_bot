from db.db import get_db_session
from db.products.model import Product
from sqlalchemy import select


async def create_product(name, price, photo, description):
    async with get_db_session() as session:
        product = Product(name=name, price=price, photo=photo, description=description)
        session.add(product)
        await session.commit()
        await session.refresh(product)  #
    return product


async def get_product(id):
    async with get_db_session() as session:
        cursor = await session.execute(select(Product).where(Product.id == id))
        return cursor.scalars().first()

async def get_all_products():
    async with get_db_session() as session:
        cursor = await session.execute(select(Product))
        return cursor.scalars().all()