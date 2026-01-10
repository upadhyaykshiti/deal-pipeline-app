from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Deal, ICDecision, Activity
from deps import require_role
import logging
# logger = get_logger("IC")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/ic", tags=["IC"])


@router.post("/deals/{deal_id}/approve")
def approve(
    deal_id: int,
    comment: str = "",
    db: Session = Depends(get_db),
    user=Depends(require_role("partner")),
):
    deal = db.query(Deal).get(deal_id)
    if not deal:
        raise HTTPException(404)

    deal.ic_status = "approved"
    deal.ic_locked = True
    deal.stage = "Invested"

    db.add_all([
        ICDecision(
            deal_id=deal_id,
            user_id=user.id,
            decision="approved",
            comment=comment,
        ),
        Activity(
            deal_id=deal_id,
            user_id=user.id,
            action="Partner approved IC",
        )
    ])

    db.commit()
    logger.info(f"IC APPROVED | deal={deal_id}")
    return {"status": "approved"}


@router.post("/deals/{deal_id}/reject")
def reject(
    deal_id: int,
    comment: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("partner")),
):
    deal = db.query(Deal).get(deal_id)
    if not deal:
        raise HTTPException(404)

    deal.ic_status = "rejected"
    deal.ic_locked = True
    deal.stage = "Passed"

    db.add_all([
        ICDecision(
            deal_id=deal_id,
            user_id=user.id,
            decision="rejected",
            comment=comment,
        ),
        Activity(
            deal_id=deal_id,
            user_id=user.id,
            action="Partner rejected IC",
        )
    ])

    db.commit()
    logger.info(f"IC REJECTED | deal={deal_id}")
    return {"status": "rejected"}
