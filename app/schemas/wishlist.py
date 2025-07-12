from pydantic import BaseModel
from typing import Optional


class WishlistItemCreate(BaseModel):
    product_id: int