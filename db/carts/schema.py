from pydantic import BaseModel, ConfigDict
from uuid import UUID
class CartCreate(BaseModel):
    user_id: int | None = None
    anonymous_id: UUID | None = None


class GetCart(BaseModel):
    id: int 
    anonymous_id: UUID
    user_id: int

class DeleteCart(BaseModel):
    anonymous_id: UUID
