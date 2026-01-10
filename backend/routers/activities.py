from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Activity
from deps import require_role, current_user

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("/deal/{deal_id}")
def get_activities(
    deal_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin", "analyst", "partner")),
):
    return (
        db.query(Activity)
        .filter(Activity.deal_id == deal_id)
        .order_by(Activity.created_at.desc())
        .all()
    )





@router.get("/latest")
def latest_activities(
    db: Session = Depends(get_db),
    user = Depends(current_user),
):
    activities = (
        db.query(Activity)
        .order_by(Activity.created_at.desc())
        .all()
    )

    latest = {}
    for a in activities:
        if a.deal_id not in latest:
            latest[a.deal_id] = a

    return latest