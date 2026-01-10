from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import ICMemoVersion, Deal
from schemas import MemoSnapshot
from database import get_db
from deps import require_role

router = APIRouter(prefix="/deals", tags=["IC Memo"])


@router.post("/{deal_id}/memo")
def save_memo(
    deal_id: int,
    data: MemoSnapshot,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "analyst"))
):
    deal = db.query(Deal).get(deal_id)
    if not deal:
        raise HTTPException(404, "Deal not found")
    
    if deal.ic_locked:
        raise HTTPException(
        status_code=403,
        detail="IC memo is locked after decision"
    )

    version = ICMemoVersion(
        deal_id=deal_id,
        snapshot=data.dict()
    )

    db.add(version)
    db.commit()
    db.refresh(version)
    return version


@router.get("/{deal_id}/memo/versions")
def versions(deal_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ICMemoVersion)
        .filter(ICMemoVersion.deal_id == deal_id)
        .order_by(ICMemoVersion.created_at.desc())
        .all()
    )


@router.get("/memo/version/{version_id}")
def get_version(version_id: int, db: Session = Depends(get_db)):
    v = db.query(ICMemoVersion).get(version_id)
    if not v:
        raise HTTPException(404, "Version not found")
    return v
