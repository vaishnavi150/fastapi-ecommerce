from pydantic import BaseModel
from typing import Optional

class ReviewCreate(BaseModel):
    review_text: str
    rating: Optional[int] = None  # 1-5

class ReviewOut(BaseModel):
    id: int
    review_text: str
    rating: Optional[int]
    product_id: int
    user_id: int

    class Config:
        orm_mode = True
