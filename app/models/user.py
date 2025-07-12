from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

    # ✅ Relationships (with other tables)
    cart = relationship("Cart", back_populates="user")
    cart_items = relationship("Cart", back_populates="user", cascade="all, delete")
    orders = relationship("Order", back_populates="user", cascade="all, delete")
    ratings = relationship("ProductRating", back_populates="user", cascade="all, delete")
    wishlist_items = relationship("Wishlist", back_populates="user", cascade="all, delete")


    