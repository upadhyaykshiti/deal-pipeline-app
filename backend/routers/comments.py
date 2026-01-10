from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Comment
from database import get_db
from deps import require_role
import logging

# logger = get_logger("COMMENTS")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/deals/{deal_id}")
def add_comment(
    deal_id: int,
    body: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("partner")),
):
    logger.info(f"Comment added | deal={deal_id} | user={user.id}")

    c = Comment(
        deal_id=deal_id,
        user_id=user.id,
        body=body,
    )
    db.add(c)
    db.commit()
    return c


@router.get("/deals/{deal_id}")
def list_comments(
    deal_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(Comment)
        .filter(Comment.deal_id == deal_id)
        .order_by(Comment.created_at.desc())
        .all()
    )
