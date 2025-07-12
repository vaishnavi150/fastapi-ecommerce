from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.auth.jwt_handler import get_current_user, get_current_admin_user
from app.schemas.order import OrderOut, OrderItemOut,OrderCreate
from typing import List
from app.models.product import Product
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/place")
def place_order(order: OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.inventory < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    total = product.price * order.quantity
    order_obj = Order(user_id=user.id, product_id=product.id, quantity=order.quantity, total_price=total)
    product.inventory -= order.quantity

    db.add(order_obj)
    db.commit()
    return {"message": "Order placed successfully"}


@router.post("/", response_model=OrderOut)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_order = Order(
        user_id=current_user.id,
        total_amount=data.total_amount,
        status="paid"  # fake payment for now
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/", response_model=List[OrderOut])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()



@router.post("/", status_code=201)
def place_order(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(item.product.price * item.quantity for item in cart_items)

    new_order = Order(user_id=current_user.id, total_amount=total)
    db.add(new_order)
    db.flush()  # to get order_id

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)

    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Order placed successfully", "order_id": new_order.id}



@router.get("/", response_model=List[OrderOut])
def user_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()

    result = []
    for order in orders:
        items = []
        for item in order.items:
            items.append({
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.product.price
            })
        result.append({
            "id": order.id,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "items": items
        })
    return result

@router.get("/all", response_model=List[OrderOut])
def all_orders(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin_user)):
    orders = db.query(Order).all()

    result = []
    for order in orders:
        items = []
        for item in order.items:
            items.append({
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.product.price
            })
        result.append({
            "id": order.id,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "items": items
        })
    return result
