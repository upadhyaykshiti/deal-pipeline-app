import logging
from fastapi import Depends, HTTPException, Header, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from auth import SECRET, ALGO
from models import User
from database import get_db


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    logger.info("➡️ current_user dependency triggered")

    if not authorization:
        logger.error("❌ Authorization header missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    logger.info(f"🔐 AUTH HEADER RECEIVED: {authorization}")

    if not authorization.startswith("Bearer "):
        logger.error("❌ Invalid Authorization header format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format"
        )

    token = authorization.split(" ", 1)[1]
    logger.info(f"🔑 JWT TOKEN: {token}")

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        logger.info(f"✅ JWT DECODED PAYLOAD: {payload}")
    except JWTError as e:
        logger.exception("❌ JWT decode failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

    user_id = payload.get("sub")
    if not user_id:
        logger.error("❌ JWT missing `sub` claim")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    logger.info(f"👤 USER ID FROM TOKEN: {user_id}")

    try:
        user = db.query(User).get(int(user_id))
    except Exception as e:
        logger.exception("❌ Failed to fetch user from DB")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID"
        )

    if not user:
        logger.error("❌ User not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    logger.info(f"AUTHENTICATED USER: id={user.id}, role={user.role}")

    return user


# Role-based access control
def require_role(*roles):
    def guard(user: User = Depends(current_user)):
        logger.info(
            f"🔒 ROLE CHECK → required={roles}, user_role={user.role}"
        )

        if user.role not in roles:
            logger.error("❌ Role authorization failed")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )

        logger.info("✅Role authorized")
        return user

    return guard
