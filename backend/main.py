from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, deals, memos, activities, ic, comments, votes, users
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ prefixes matter
app.include_router(auth.router, prefix="/auth")
app.include_router(deals.router)
app.include_router(memos.router, prefix="/memos")
app.include_router(activities.router)
app.include_router(ic.router)
app.include_router(comments.router)
app.include_router(votes.router)
app.include_router(users.router)






