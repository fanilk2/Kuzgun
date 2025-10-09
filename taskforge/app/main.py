"""TaskForge FastAPI application."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Generator, Iterable, List

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from . import models
from .db import SessionLocal, init_db
from .rules_engine import calculate_score


app = FastAPI(title="TaskForge")

WEB_DIR = Path(__file__).resolve().parent.parent / "web"
if WEB_DIR.exists():
    app.mount("/web", StaticFiles(directory=str(WEB_DIR)), name="web")


@app.get("/", response_class=HTMLResponse)
def web_home() -> str:
    if not WEB_DIR.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UI bulunamadi")
    return (WEB_DIR / "index.html").read_text(encoding="utf-8")

_scheduler = BackgroundScheduler(timezone="UTC")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _ensure_scheduler_started() -> None:
    if not _scheduler.running:
        _scheduler.start()


def _hourly_reminder_job() -> None:
    db = SessionLocal()
    try:
        reminder = models.Reminder(message="Yeni bir gorev kaydetmeyi unutma!")
        db.add(reminder)
        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    _ensure_scheduler_started()
    _scheduler.add_job(
        _hourly_reminder_job,
        "interval",
        hours=1,
        id="hourly-reminder",
        replace_existing=True,
        next_run_time=datetime.utcnow(),
    )


@app.on_event("shutdown")
def on_shutdown() -> None:
    if _scheduler.running:
        _scheduler.shutdown(wait=False)


@app.get("/api/ping")
def ping() -> dict[str, str]:
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Activity endpoints
# ---------------------------------------------------------------------------


class ActivityCreate(BaseModel):
    name: str
    category: str | None = None
    points_per_10_min: int = Field(
        ..., description="Positive for productive tasks, negative for bad habits."
    )


class ActivityOut(BaseModel):
    id: int
    name: str
    category: str | None
    points_per_10_min: int

    class Config:
        from_attributes = True


@app.post("/api/activities", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
def create_or_update_activity(payload: ActivityCreate, db: Session = Depends(get_db)):
    activity = db.query(models.Activity).filter_by(name=payload.name).first()

    if activity:
        activity.category = payload.category
        activity.points_per_10_min = payload.points_per_10_min
    else:
        activity = models.Activity(
            name=payload.name,
            category=payload.category,
            points_per_10_min=payload.points_per_10_min,
        )
        db.add(activity)

    db.commit()
    db.refresh(activity)
    return activity


@app.get("/api/activities", response_model=List[ActivityOut])
def list_activities(db: Session = Depends(get_db)) -> List[ActivityOut]:
    items = db.query(models.Activity).order_by(models.Activity.name.asc()).all()
    return [ActivityOut.model_validate(item) for item in items]


# ---------------------------------------------------------------------------
# Entry endpoints
# ---------------------------------------------------------------------------


class EntryCreate(BaseModel):
    activity_name: str
    duration_min: int = Field(..., ge=1, description="Total minutes spent on the activity.")
    category: str | None = None
    note: str | None = None
    tags: list[str] = Field(default_factory=list)
    started_at: datetime | None = None


class EntryOut(BaseModel):
    id: int
    activity: str
    category: str | None
    started_at: datetime
    duration_min: int
    score_delta: int
    note: str | None = None
    tags: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True


def _serialize_tags(tags: Iterable[str]) -> str:
    normalized = [tag.strip() for tag in tags if tag.strip()]
    return ",".join(normalized)


def _deserialize_tags(tags_csv: str | None) -> list[str]:
    if not tags_csv:
        return []
    return [part.strip() for part in tags_csv.split(",") if part.strip()]


def _resolve_activity(db: Session, payload: EntryCreate) -> models.Activity:
    activity = db.query(models.Activity).filter_by(name=payload.activity_name).first()
    if activity:
        if payload.category and payload.category != activity.category:
            activity.category = payload.category
            db.add(activity)
        return activity

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=(
            "Bu aktivite sistemde kayitli degil. Once /api/activities "
            "uzerinden puan bilgisini girerek aktivite olusturmalisin."
        ),
    )


@app.post("/api/entries", response_model=EntryOut, status_code=status.HTTP_201_CREATED)
def create_entry(payload: EntryCreate, db: Session = Depends(get_db)):
    activity = _resolve_activity(db, payload)

    started_at = payload.started_at or datetime.utcnow()
    score_from_activity = (payload.duration_min // 10) * activity.points_per_10_min
    rule_adjustment = calculate_score(
        activity=activity.name,
        duration_min=payload.duration_min,
        category=payload.category or activity.category,
        tags=payload.tags,
    )
    total_score = score_from_activity + rule_adjustment

    entry = models.Entry(
        activity_id=activity.id,
        duration_min=payload.duration_min,
        started_at=started_at,
        score_delta=total_score,
        note=payload.note,
        tags_csv=_serialize_tags(payload.tags),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return EntryOut(
        id=entry.id,
        activity=activity.name,
        category=activity.category,
        started_at=entry.started_at,
        duration_min=entry.duration_min,
        score_delta=entry.score_delta,
        note=entry.note,
        tags=_deserialize_tags(entry.tags_csv),
    )


@app.get("/api/entries", response_model=List[EntryOut])
def list_entries(db: Session = Depends(get_db)) -> List[EntryOut]:
    rows = db.query(models.Entry).order_by(models.Entry.started_at.desc()).limit(100).all()
    output: list[EntryOut] = []
    for entry in rows:
        output.append(
            EntryOut(
                id=entry.id,
                activity=entry.activity.name if entry.activity else "",
                category=entry.activity.category if entry.activity else None,
                started_at=entry.started_at,
                duration_min=entry.duration_min,
                score_delta=entry.score_delta,
                note=entry.note,
                tags=_deserialize_tags(entry.tags_csv),
            )
        )
    return output


class DailySummary(BaseModel):
    date: date
    total_minutes: int
    total_score: int


@app.get("/api/daily-summary", response_model=DailySummary)
def daily_summary(day: date | None = None, db: Session = Depends(get_db)) -> DailySummary:
    target_day = day or date.today()
    start = datetime.combine(target_day, datetime.min.time())
    end = datetime.combine(target_day, datetime.max.time())

    rows = (
        db.query(models.Entry)
        .filter(models.Entry.started_at >= start, models.Entry.started_at <= end)
        .all()
    )

    total_minutes = sum(row.duration_min for row in rows)
    total_score = sum(row.score_delta for row in rows)

    return DailySummary(date=target_day, total_minutes=total_minutes, total_score=total_score)


# ---------------------------------------------------------------------------
# Reminder endpoints
# ---------------------------------------------------------------------------


class ReminderOut(BaseModel):
    id: int
    message: str
    created_at: datetime
    acknowledged: bool

    class Config:
        from_attributes = True


@app.get("/api/reminders", response_model=List[ReminderOut])
def list_reminders(db: Session = Depends(get_db)) -> List[ReminderOut]:
    reminders = db.query(models.Reminder).order_by(models.Reminder.created_at.desc()).limit(50).all()
    return [ReminderOut.model_validate(reminder) for reminder in reminders]


@app.post("/api/reminders/{reminder_id}/ack", status_code=status.HTTP_204_NO_CONTENT)
def acknowledge_reminder(reminder_id: int, db: Session = Depends(get_db)) -> None:
    reminder = db.query(models.Reminder).filter_by(id=reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hatirlatma bulunamadi")

    reminder.acknowledged = True
    db.add(reminder)
    db.commit()
