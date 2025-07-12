from fastapi import APIRouter,Depends,HTTPException,Query 
from sqlalchemy.orm import Session 
from typing import List,Optional 
from app.database.connection import get_db 
from app.models.product import Product 
from app.schemas.product import ProductCreate,ProductOut
from app.auth.jwt_handler import get_current_user,get_current_admin_user
from app.models.user import User
from fastapi import File, UploadFile
import shutil
import os
from uuid import uuid4

router = APIRouter(prefix="/products",tags=["Products"])

@router.post("/", response_model=ProductOut)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # 🛡️ Only admin allowed
):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/", response_model=List[ProductOut])
def list_products(
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())

    return query.all()
@router.get("/top-rated", response_model=List[ProductOut])
def get_top_rated_products(
    limit: int = 5,
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if min_price:
        query = query.filter(Product.price >= min_price)

    products = query.order_by(Product.avg_rating.desc()).limit(limit).all()
    return products



UPLOAD_DIR = "uploads"

@router.post("/upload-image/")
def upload_image(file: UploadFile = File(...)):
    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/{UPLOAD_DIR}/{filename}"
    return {"image_url": image_url}
