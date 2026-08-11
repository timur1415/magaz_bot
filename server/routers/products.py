
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from config.logger import logger
from db.products.crud import create, get_all, get_by_id
from db.products.schema import ProductCreate, ProductRead
from server.deps import SessionDep

UPLOADS_DIR = Path("static/uploads")
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(
    prefix="/products",
    tags=["products"])

@router.get("")
async def get_products(session: SessionDep) -> list[ProductRead]:
    products = await get_all(session)
    return products

@router.post("")
async def create_product(
    session: SessionDep,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    photo: UploadFile = File(...),
) -> ProductRead:
    ext = Path(photo.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    file_path = UPLOADS_DIR / filename
    content = await photo.read()
    file_path.write_bytes(content)
    data = ProductCreate(name=name, description=description, price=price, photo=str(file_path))
    logger.info(f"{data}")
    product = await create(session, data)
    return product

@router.get('/{product_id}')
async def get_product(product_id: int, session: SessionDep) -> ProductRead:
    product = await get_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product






















    