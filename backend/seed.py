from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User, Deal, ICMemoVersion
from auth import hash_pw
from datetime import datetime

def seed_users(db: Session):
    users = [
        ("admin@example.com", "admin"),
        ("analyst@example.com", "analyst"),
        ("partner@example.com", "partner"),
    ]

    for email, role in users:
        exists = db.query(User).filter(User.email == email).first()
        if not exists:
            user = User(
                email=email,
                password_hash=hash_pw("password"),
                role=role
            )
            db.add(user)
            print(f"✅ Created {role}: {email}")
        else:
            print(f"ℹ️ User already exists: {email}")

    db.commit()


def seed_deals(db: Session):
    if db.query(Deal).count() > 0:
        print("ℹ️ Deals already exist")
        return

    deal = Deal(
        name="Acme AI",
        company_url="https://acme.ai",
        stage="IC",
        round="Seed",
        check_size="$500k",
        status="Under Review",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(deal)
    db.commit()
    db.refresh(deal)

    print(f"✅ Created deal: {deal.name}")
    return deal


def seed_memo(db: Session, deal: Deal):
    if not deal:
        return

    exists = (
        db.query(ICMemoVersion)
        .filter(ICMemoVersion.deal_id == deal.id)
        .first()
    )

    if exists:
        print("ℹ️ Memo already exists")
        return

    memo = ICMemoVersion(
        deal_id=deal.id,
        snapshot={
            "summary": "AI-powered workflow automation",
            "market": "Large and growing SMB market",
            "product": "B2B SaaS platform",
            "traction": "100+ paying customers",
            "risks": "Highly competitive space",
            "open_questions": "Go-to-market scalability"
        },
        created_at=datetime.utcnow()
    )

    db.add(memo)
    db.commit()

    print("✅ Created initial IC memo")


def main():
    db = SessionLocal()

    try:
        seed_users(db)
        deal = seed_deals(db)
        seed_memo(db, deal)
    finally:
        db.close()


if __name__ == "__main__":
    main()
