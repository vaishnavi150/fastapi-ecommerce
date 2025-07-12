# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database.connection import get_db
# from app.auth.jwt_handler import get_current_user
# from app.models.wishlist import Wishlist
# from app.models.product import Product
# from app.schemas.wishlist import WishlistItemCreate

# wishlist_router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

# @wishlist_router.post("/add")
# def add_to_wishlist(item: WishlistItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
#     product = db.query(Product).filter(Product.id == item.product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")

#     exists = db.query(Wishlist).filter(Wishlist.user_id == user.id, Wishlist.product_id == item.product_id).first()
#     if exists:
#         return {"message": "Already in wishlist"}

#     wishlist_item = Wishlist(user_id=user.id, product_id=item.product_id)
#     db.add(wishlist_item)
#     db.commit()
#     return {"message": "Added to wishlist"}



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth.jwt_handler import get_current_user
from app.models.user import User
from app.models.wishlist import Wishlist
from app.models.product import Product
from typing import List

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

@router.post("/{product_id}")
def add_to_wishlist(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    exists = db.query(Wishlist).filter_by(user_id=current_user.id, product_id=product_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Already in wishlist")

    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.add(Wishlist(user_id=current_user.id, product_id=product_id))
    db.commit()
    return {"message": "Added to wishlist"}

@router.get("/", response_model=List[int])
def get_wishlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return [item.product_id for item in db.query(Wishlist).filter_by(user_id=current_user.id).all()]

@router.delete("/{product_id}")
def remove_from_wishlist(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Wishlist).filter_by(user_id=current_user.id, product_id=product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in wishlist")

    db.delete(item)
    db.commit()
    return {"message": "Removed from wishlist"}
