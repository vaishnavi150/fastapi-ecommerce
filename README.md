# 🛍️ FastAPI Ecommerce

A modern and scalable backend system for an e-commerce platform, built with **FastAPI**, **SQLAlchemy**, and **JWT authentication**. This project supports essential e-commerce features like product management, user authentication, cart, wishlist, orders, ratings, and image uploads.

---

## 🚀 Features

- ✅ User Registration & Login with JWT Authentication (Access + Refresh Tokens)
- 🔐 Role-based access control (Admin / User)
- 🛒 Product listing, search, filter, sort
- ❤️ Wishlist management
- 🛍️ Cart system with quantity control
- ⭐ Product rating and "Top Rated Products"
- 📦 Order placement and tracking
- 💳 Checkout system
- 🖼️ Product image upload support
- 📁 Clean project structure following FastAPI best practices

---


---

## 🔧 Tech Stack

- **FastAPI** – High-performance web framework
- **SQLAlchemy** – ORM for database interactions
- **PostgreSQL / SQLite** – Relational database
- **Pydantic v2** – Data validation and serialization
- **JWT (PyJWT)** – Token-based authentication
- **Uvicorn** – ASGI server for development

---

## 🔑 Authentication

- **Access Token** – Short-lived token for user access
- **Refresh Token** – Long-lived token to get new access tokens
- Admin-only routes are protected (e.g., Add Product)

---

## ▶️ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/fastapi-ecommerce.git
cd fastapi-ecommerce
```
---
### 2. Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
---

### 4. Run the server
```bash
uvicorn app.main:app --reload
```
---
# 📷 Image Upload
Uploaded product images are stored in the /uploads folder and accessible via static routes.


---

### 
API Testing
Use the interactive Swagger UI:
```bash
http://localhost:8000/docs
```
---
✨ Future Enhancements

Stripe/Razorpay Payment Integration

Email-based password reset (Forget Password)

Admin dashboard UI

Frontend (React/HTML+CSS)
----









