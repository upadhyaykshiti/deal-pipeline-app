
from pydantic import BaseModel
from typing import Dict

class DealCreate(BaseModel):
    name: str
    company_url: str
    stage: str
    round: str
    check_size: int
    status: str


class MemoSnapshot(BaseModel):
    summary: str
    market: str
    product: str
    traction: str
    risks: str
    open_questions: str
    
class CommentIn(BaseModel):
    body: str

class VoteIn(BaseModel):
    decision: str  # yes | no

class ICDecisionIn(BaseModel):
    comment: str | None = None