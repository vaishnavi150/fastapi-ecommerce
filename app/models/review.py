from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class ProductReview(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    review_text = Column(String(1000))
    rating = Column(Integer)  # optional

    user = relationship("User")
    product = relationship("Product", backref="reviews")
