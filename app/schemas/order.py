from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional
from datetime import datetime



class OrderCreate(BaseModel):
    product_id: int
    quantity: int



class OrderItemOut(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float

class OrderOut(BaseModel):
    id: int
    total_amount: float
    created_at: datetime
    status: str
    items: List[OrderItemOut]
    class Config:
        orm_mode = True
