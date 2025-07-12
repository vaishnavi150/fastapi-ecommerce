from pydantic import BaseModel
from typing import Optional
class CartAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(BaseModel):
    product_id: int
    quantity: Optional[int] = 1

class CartUpdate(BaseModel):
    quantity: int

class CartOut(BaseModel):
    product_id: int
    product_name: str
    price: float
    quantity: int
    total: float
