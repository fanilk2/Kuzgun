from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
from typing import List
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import init_db, SessionLocal
from app import models
from typing import List
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models

app= FastAPI(title="Taskforge")
@app.on_event("startup")
def on_startup():
    init_db()
@app.get("/api/ping")
def ping():
    return{"status":"ok"}
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close
class EntryCreate(BaseModel):
    username: str
    activity: str
    category: str | None=None
    duration_min: int=0
    note: str | None = None
    tags: list[str] = []
    
class EntryOut(BaseModel):
    id: int
    activity: str
    started_at: str
    duration_min: int
    score_delta: int
    note: str | None = None
    tags_csv: str | None = None
    class Config:
        from_attritubes=True
def get_or_create_user(db: Session, username: str):
    u = db.query(models.User).filter_by(username=username).first()
    if not u:
        u = models.User(username=username, password_hash="x")
        db.add(u)
        db.commit()
        db.refresh(u)
    return u
def get_or_create_activity(db: Session, name: str, category: str | None):
    a = db.query(models.Activity).filter_by(name=name).first()
    if not a:
        a = models.Activity(name=name, category=category or "", base_score=0)
        db.add(a)
        db.commit()
        db.refresh(a)
    return a
# --- POST /api/entries : kayıt oluştur
@app.post("/api/entries", response_model=EntryOut)
def create_entry(payload: EntryCreate, db: Session = Depends(get_db)):
    user = get_or_create_user(db, payload.username)
    activity = get_or_create_activity(db, payload.activity, payload.category)

    entry = models.Entry(
        user_id=user.id,
        activity_id=activity.id,
        duration_min=payload.duration_min,
        note=payload.note,
        tags_csv=",".join(payload.tags) if payload.tags else None,
        score_delta=0,  # şimdilik kural motoru yok; sonra hesaplayacağız
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    # response_model için düz alanlara map
    return EntryOut(
        id=entry.id,
        activity=activity.name,
        started_at=entry.started_at.isoformat(),
        duration_min=entry.duration_min,
        score_delta=entry.score_delta,
        note=entry.note,
        tags_csv=entry.tags_csv,
    )

# --- GET /api/entries : son kayıtlar
@app.get("/api/entries", response_model=List[EntryOut])
def list_entries(db: Session = Depends(get_db)):
    rows = db.query(models.Entry).order_by(models.Entry.id.desc()).limit(50).all()
    out: list[EntryOut] = []
    for e in rows:
        out.append(
            EntryOut(
                id=e.id,
                activity=e.activity.name if e.activity else "",
                started_at=e.started_at.isoformat(),
                duration_min=e.duration_min,
                score_delta=e.score_delta,
                note=e.note,
                tags_csv=e.tags_csv,
            )
        )
    return out
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)
    base_score = Column(Integer, default=0)

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    duration_min = Column(Integer, default=0)
    note = Column(Text)
    tags_csv = Column(String)
    score_delta = Column(Integer, default=0)

    user = relationship("User")
    activity = relationship("Activity")
