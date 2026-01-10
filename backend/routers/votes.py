from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Vote, Deal
from database import get_db
from deps import require_role
import logging

# logger = get_logger("VOTES")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/deals/{deal_id}")
def cast_vote(
    deal_id: int,
    decision: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("partner")),
):
    logger.info(f"Vote attempt | deal={deal_id} | user={user.id}")

    deal = db.query(Deal).get(deal_id)
    if not deal:
        raise HTTPException(404, "Deal not found")

    if deal.ic_locked:
        raise HTTPException(403, "IC is locked")

    vote = Vote(
        deal_id=deal_id,
        user_id=user.id,
        decision=decision,
    )
    db.add(vote)
    db.commit()

    logger.info(f"Vote saved | deal={deal_id} | user={user.id}")
    return vote


@router.get("/deals/{deal_id}")
def list_votes(
    deal_id: int,
    db: Session = Depends(get_db),
):
    return db.query(Vote).filter(Vote.deal_id == deal_id).all()
