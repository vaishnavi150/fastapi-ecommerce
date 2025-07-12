from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Wishlist(Base):
    __tablename__ = "wishlist"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='unique_wishlist'),)

    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product")
