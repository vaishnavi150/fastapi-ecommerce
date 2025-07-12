from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.auth.jwt_handler import get_current_user, get_current_admin_user
from app.schemas.review import ReviewCreate, ReviewOut
from app.models.review import ProductReview
from app.models.user import User
from app.models.product import Product

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/{product_id}", response_model=ReviewOut)
def submit_review(product_id: int, data: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    review = ProductReview(
        product_id=product_id,
        user_id=current_user.id,
        review_text=data.review_text,
        rating=data.rating
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("/{product_id}", response_model=List[ReviewOut])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    return db.query(ProductReview).filter_by(product_id=product_id).all()

@router.get("/admin/all", response_model=List[ReviewOut])
def get_all_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    return db.query(ProductReview).all()
