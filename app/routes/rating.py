from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.rating import  ProductRating
from app.models.product import Product
from app.auth.jwt_handler import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/{product_id}")
def rate_product(product_id: int, rating: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Allow only one rating per user per product
    existing = db.query(ProductRating).filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        existing.rating = rating
    else:
        db.add(ProductRating(user_id=current_user.id, product_id=product_id, rating=rating))

    db.commit()

    # Recalculate avg_rating
    ratings = db.query(ProductRating).filter_by(product_id=product_id).all()
    avg = sum(r.rating for r in ratings) / len(ratings)
    product.avg_rating = round(avg, 1)
    db.commit()

    return {"message": "Rating submitted", "new_avg": product.avg_rating}
