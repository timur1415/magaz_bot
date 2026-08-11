from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    photo: str
    description: str
    price: float

class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    photo: str
    description: str
    price: float

class ProductUpdate(BaseModel):
    name: str | None = None
    photo: str | None = None
    description: str | None = None
    price: float | None = None