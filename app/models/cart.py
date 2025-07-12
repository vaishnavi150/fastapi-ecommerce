
from sqlalchemy import Column, Integer, ForeignKey,Float,String
from sqlalchemy.orm import relationship
from app.database.connection import Base



class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    user = relationship("User", back_populates="cart")



# class Wishlist(Base):
#     __tablename__ = "wishlists"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     product_id = Column(Integer, ForeignKey("products.id"))


# class Order(Base):
#     __tablename__ = "orders"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     product_id = Column(Integer, ForeignKey("products.id"))
#     quantity = Column(Integer)
#     total_price = Column(Float)
#     status = Column(String, default="pending")








# class Cart(Base):
#     __tablename__ = "cart"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
#     quantity = Column(Integer, default=1)

#     user = relationship("User", back_populates="cart_items")
#     product = relationship("Product")
