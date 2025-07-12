# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from app.database.connection import get_db
# from app.auth.jwt_handler import get_current_user
# from app.models.cart import Cart
# from app.schemas.cart import CartAdd, CartUpdate, CartOut
# from app.models.user import User

# router = APIRouter(prefix="/cart", tags=["Cart"])

# @router.post("/add")
# def add_to_cart(data: CartAdd, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     cart_item = db.query(Cart).filter_by(user_id=current_user.id, product_id=data.product_id).first()
#     if cart_item:
#         cart_item.quantity += data.quantity
#     else:
#         new_item = Cart(user_id=current_user.id, product_id=data.product_id, quantity=data.quantity)
#         db.add(new_item)
#     db.commit()
#     return {"message": "Item added to cart"}

# @router.get("/", response_model=List[CartOut])
# def view_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     cart_items = db.query(Cart).filter_by(user_id=current_user.id).all()
#     output = []
#     for item in cart_items:
#         output.append({
#             "product_id": item.product.id,
#             "product_name": item.product.name,
#             "price": item.product.price,
#             "quantity": item.quantity,
#             "total": item.product.price * item.quantity
#         })
#     return output

# @router.put("/update/{product_id}")
# def update_cart(product_id: int, data: CartUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     cart_item = db.query(Cart).filter_by(user_id=current_user.id, product_id=product_id).first()
#     if not cart_item:
#         raise HTTPException(status_code=404, detail="Item not in cart")
#     cart_item.quantity = data.quantity
#     db.commit()
#     return {"message": "Cart updated"}

# @router.delete("/remove/{product_id}")
# def remove_cart_item(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     cart_item = db.query(Cart).filter_by(user_id=current_user.id, product_id=product_id).first()
#     if not cart_item:
#         raise HTTPException(status_code=404, detail="Item not in cart")
#     db.delete(cart_item)
#     db.commit()
#     return {"message": "Item removed from cart"}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth.jwt_handler import get_current_user
from app.models.cart import Cart
from app.models.product import Product
from app.schemas.cart import CartItemCreate

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/add")
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = db.query(Cart).filter(Cart.user_id == user.id, Cart.product_id == item.product_id).first()
    if existing:
        existing.quantity += item.quantity
    else:
        new_item = Cart(user_id=user.id, product_id=item.product_id, quantity=item.quantity)
        db.add(new_item)

    db.commit()
    return {"message": "Product added to cart"}