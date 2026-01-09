from fastapi import APIRouter, Depends, HTTPException
from models import User
from database import get_db
from deps import require_role
from auth import hash_pw

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users")
def list_users(db=Depends(get_db), user=Depends(require_role("admin"))):
    return db.query(User).all()



@router.post("/users")
def create_user(
    email: str,
    password: str,
    role: str,
    db=Depends(get_db),
    user=Depends(require_role("admin"))
):
    if role not in ["admin", "analyst", "partner"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    u = User(
        email=email,
        password_hash=hash_pw(password),
        role=role
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u



@router.patch("/users/{user_id}")
def update_user_role(
    user_id: int,
    role: str,
    db=Depends(get_db),
    user=Depends(require_role("admin"))
):
    if role not in ["admin", "analyst", "partner"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    u = db.query(User).get(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")

    u.role = role
    db.commit()
    return {"status": "updated"}


@router.patch("/users/{user_id}/password")
def reset_password(
    user_id: int,
    password: str,
    db=Depends(get_db),
    user=Depends(require_role("admin"))
):
    u = db.query(User).get(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")

    u.password_hash = hash_pw(password)
    db.commit()
    return {"status": "password reset"}



@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db=Depends(get_db),
    user=Depends(require_role("admin"))
):
    u = db.query(User).get(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(u)
    db.commit()
    return {"status": "deleted"}
