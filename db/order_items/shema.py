from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderItemGet(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
