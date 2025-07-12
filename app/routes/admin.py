from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import get_db
from app.auth.jwt_handler import get_current_admin_user
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.product import Product

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def get_dashboard_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    total_orders = db.query(func.count(Order.id)).scalar()
    total_customers = db.query(func.count(User.id)).scalar()
    total_revenue = db.query(func.sum(Order.total_price)).scalar() or 0.0

    # Top 5 products
    top_products = (
        db.query(
            Product.name,
            func.sum(OrderItem.quantity).label("total_quantity")
        )
        .join(OrderItem.product)
        .group_by(Product.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )

    return {
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_revenue": round(total_revenue, 2),
        "top_products": [{"name": name, "sold": qty} for name, qty in top_products]
    }
