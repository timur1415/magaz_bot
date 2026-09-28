from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.cart_items.models import CartItem  # noqa: F401
from db.carts.model import Cart  # noqa: F401
from db.products.model import Product  # noqa: F401
from db.users.model import User  # noqa: F401

#'sqlite+aiosqlite://user:password@host:port/db'
engine = create_async_engine('sqlite+aiosqlite:///magaz.db', echo=True)



async_session_maker = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # Создавать все таблицы в базе данных
