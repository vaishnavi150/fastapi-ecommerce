from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    price = Column(Float)
    image_url = Column(String, nullable=True)
    tags = Column(String)
    avg_rating = Column(Float, default=0.0)
    inventory = Column(Integer, default=10)  # Add inventory support
    ratings = relationship("ProductRating", back_populates="product", cascade="all, delete")
