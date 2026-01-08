from sqlalchemy import *
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # admin | analyst | partner


class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    company_url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    stage = Column(String)
    round = Column(String)
    check_size = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class ICMemo(Base):
    __tablename__ = "ic_memos"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))


class ICMemoVersion(Base):
    __tablename__ = "ic_memo_versions"
    id = Column(Integer, primary_key=True)
    memo_id = Column(Integer)
    snapshot = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer)
    user_id = Column(Integer)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer)
    user_id = Column(Integer)
    decision = Column(String)  # approve | decline
    created_at = Column(DateTime, default=datetime.utcnow)
