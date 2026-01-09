from sqlalchemy import *
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # admin | analyst | partner


# class Deal(Base):
#     __tablename__ = "deals"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     company_url = Column(String)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     # stage = Column(String)
#     stage = Column(String, nullable=False, default="Sourced")
#     round = Column(String)
#     check_size = Column(Integer)
#     status = Column(String)
#     ic_status = Column(
#     String,
#     nullable=False,
#     server_default="pending"
#     )
#     ic_locked = Column(
#         Boolean,
#         nullable=False,
#         server_default="false"
#     )

#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow)
class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    company_url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    stage = Column(String, nullable=False, default="Sourced")
    round = Column(String)
    check_size = Column(Integer)
    status = Column(String)

    ic_status = Column(
        String,
        nullable=False,
        server_default=text("'pending'")
    )

    ic_locked = Column(
        Boolean,
        nullable=False,
        server_default=text("0")
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)



class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ICMemo(Base):
    __tablename__ = "ic_memos"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))


class ICMemoVersion(Base):
    __tablename__ = "ic_memo_versions"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    snapshot = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class ICDecision(Base):
    __tablename__ = "ic_decisions"

    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    decision = Column(String)  # approved | rejected
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)



class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    decision = Column(String)  # approve | decline
    created_at = Column(DateTime, default=datetime.utcnow)
