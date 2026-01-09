import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Deal, Activity
from deps import require_role

router = APIRouter(prefix="/deals", tags=["Deals"])
logger = logging.getLogger("deals")

@router.get("/")
def list_deals(db: Session = Depends(get_db)):
    return db.query(Deal).all()


@router.post("/")
def create_deal(
    data: dict,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin", "analyst")),
):
    if "name" not in data:
        raise HTTPException(400, "name is required")

    deal = Deal(
        name=data["name"],
        stage="Sourced",
        owner_id=user.id,
    )

    db.add(deal)
    db.commit()
    db.refresh(deal)

    return deal


@router.post("/{deal_id}/move")
def move_deal(
    deal_id: int,
    stage: str,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin", "analyst")),
):
    logger.info(f"Move deal request: deal_id={deal_id}, stage={stage}")

    deal = db.query(Deal).get(deal_id)
    if not deal:
        logger.error(f"Deal {deal_id} not found")
        raise HTTPException(status_code=404, detail="Deal not found")

    old_stage = deal.stage
    logger.info(f"Changing stage: {old_stage} → {stage}")

    deal.stage = stage

    activity = Activity(
        deal_id=deal.id,
        user_id=user.id,
        action=f"Moved deal from {old_stage} → {stage}",
    )

    db.add(activity)

    try:
        db.commit()
        logger.info("Deal moved + activity logged")
    except Exception as e:
        logger.exception("DB commit failed")
        db.rollback()
        raise HTTPException(status_code=500, detail="DB error")

    return {"ok": True}