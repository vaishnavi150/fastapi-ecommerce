from pydantic import BaseModel,ConfigDict
from typing import List,Optional 

class ProductCreate(BaseModel):
    name : str
    description : str
    category : str
    price:float 
    image_url : str 
    tags: Optional[str] = ""



class ProductOut(ProductCreate):
    id:int 
    name:str
    price:float 
    description:str
    category: Optional[str]
    tags: Optional[str]
    avg_rating: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

    