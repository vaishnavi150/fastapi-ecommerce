from pydantic import BaseModel,EmailStr, ConfigDict

class UserCreate(BaseModel):
    name:str 
    email:EmailStr 
    password:str 

class UserLogin(BaseModel):
    email:EmailStr 
    password:str 

class UserOut(BaseModel):
    id:int
    name:str 
    email:EmailStr 
    is_admin:bool
    model_config = ConfigDict(from_attributes=True)



    
