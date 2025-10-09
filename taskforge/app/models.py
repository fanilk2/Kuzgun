"""SQLAlchemy models for TaskForge."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .db import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=True)
    points_per_10_min = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    entries = relationship("Entry", back_populates="activity")


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    duration_min = Column(Integer, default=0, nullable=False)
    score_delta = Column(Integer, default=0, nullable=False)
    note = Column(Text, nullable=True)
    tags_csv = Column(String, nullable=True)

    activity = relationship("Activity", back_populates="entries")


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    acknowledged = Column(Boolean, default=False, nullable=False)
