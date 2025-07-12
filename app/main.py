from fastapi import FastAPI
from app.routes import auth,product
from app.database.connection import Base, engine
from app.routes import cart  
from app.routes import order
from app.routes import rating
from app.routes import wishlist, review
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
os.makedirs("uploads", exist_ok=True)
# Create tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(rating.router)
app.include_router(wishlist.router)
app.include_router(review.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Welcome to ShopZenith API 🚀"}
