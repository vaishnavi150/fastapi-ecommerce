from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class ProductRating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer)  # 1 to 5

    product = relationship("Product", back_populates="ratings")
    user = relationship("User", back_populates="ratings") 
