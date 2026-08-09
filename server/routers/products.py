
from fastapi import APIRouter, HTTPException

from db.products.crud import create, get_all, get_by_id, update, delete
from db.products.schema import ProductCreate, ProductRead
from server.deps import SessionDep

router = APIRouter(
    prefix="/products",
    tags=["products"])

@router.get("")
async def get_products(session: SessionDep) -> list[ProductRead]:
    products = await get_all(session)
    return products

@router.post("")
async def create_product(session: SessionDep, data: ProductCreate) -> ProductRead:
    product = await create(session, data)
    return product

@router.get('/{product_id}')
async def get_product(product_id: int, session: SessionDep) -> ProductRead:
    product = await get_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/add")
async def add_product():
    return {"message": "Add product page"}  



















    