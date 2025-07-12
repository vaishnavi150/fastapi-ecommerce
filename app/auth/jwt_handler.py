from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi import Depends,HTTPException,status 
from jose import JWTError,jwt
from sqlalchemy.orm import Session 
from app.database.connection import get_db 
from app.models.user import User 
from fastapi.security import OAuth2PasswordBearer 


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data:dict):
    to_encode = data.copy()
    expire  =datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)




def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("Token received:", token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        print("Decoded payload:", payload)
        user_id: int = payload.get("user_id")
        is_admin: bool = payload.get("is_admin", False)
        if user_id is None:
            print("user_id missing")
            raise credentials_exception
    except JWTError as e:
        print("JWTError:", str(e))
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        print("User not found in DB")
        raise credentials_exception

    user.is_admin = is_admin
    print("User returned:", user.email)
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only. Access denied.",
        )
    return current_user
