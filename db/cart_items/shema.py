from pydantic import BaseModel, ConfigDict

class CartItemCreate(BaseModel):
    cart_id: int
    product_id: int
    quantity: int


class CartItemGet(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int

