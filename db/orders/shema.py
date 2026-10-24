from uuid import UUID

from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int | None = None
    anonymous_id: UUID | None = None
    address: str
    phone: str


class OrderGet(BaseModel):
    id: int 
    anonymous_id: UUID
    user_id: int