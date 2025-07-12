from fastapi import APIRouter,Depends,HTTPException,status 
from sqlalchemy.orm import Session 
from app.schemas.user import UserCreate,UserLogin,UserOut 
from app.models.user import User 
from app.database.connection import get_db 
from app.utils.hash import hash_password,verify_password 
from app.auth.jwt_handler import create_access_token 
from app.auth.jwt_handler import get_current_user
from app.schemas.product import ProductCreate,ProductOut
from app.models.product import Product 



router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=UserOut,status_code=status.HTTP_201_CREATED)
def register(user:UserCreate,db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException (status_code=400,detail="Email already registered")
    
    try:
        hashed_pw = hash_password(user.password)
        new_user = User(
            name = user.name,
            email = user.email,
            hashed_password = hashed_pw
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user 
    
    except Exception as e:
        print("ERROR",str(e))
        db.rollback()
        raise HTTPException(status_code=500,detail="Internal Server Error")
    

@router.post("/login")
def login(user:UserLogin,db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email==user.email).first()
    if not db_user or not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid credentails")
    
    token = create_access_token(data={"user_id":db_user.id,"is_admin":db_user.is_admin})
    return{"access_token":token,"token_type":"bearer"}

@router.get("/me", response_model=UserOut)
def read_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/", response_model=ProductOut, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can add products")

    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


