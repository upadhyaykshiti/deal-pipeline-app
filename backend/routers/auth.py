from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_pw, verify_pw, create_token
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

# class SignupRequest(BaseModel):
#     email: str
#     password: str
#     role: str

# @router.post("/signup")
# def signup(data: SignupRequest, db: Session = Depends(get_db)):
#     user = User(
#         email=data.email,
#         password_hash=hash_pw(data.password),
#         role=data.role,
#     )
#     db.add(user)
#     db.commit()
#     return {"ok": True}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_pw(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "token": create_token(user),
        "role": user.role,
    }
