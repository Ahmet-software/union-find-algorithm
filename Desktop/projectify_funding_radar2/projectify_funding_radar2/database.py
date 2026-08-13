"""
database.py
SQLite + SQLAlchemy veritabanı katmanı.

Tablolar:
  - profiles          : aktif kullanıcı profili (user_type + JSON veri)
  - project_summaries : proje özeti (JSON veri)
  - funding_calls     : taranan çağrılar (FundingCall)
  - match_results     : uygunluk skor sonuçları (MatchResult)

Not: 'Clear / Taramaları Sil' yalnızca funding_calls ve match_results
tablolarını boşaltır; profiles ve project_summaries korunur.
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


# --------------------------------------------------------------------------
# ORM Tabloları
# --------------------------------------------------------------------------
class ProfileRow(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_type = Column(String(32), nullable=False)
    data_json = Column(Text, nullable=False)  # profilin JSON hali
    created_at = Column(DateTime, default=datetime.utcnow)


class ProjectSummaryRow(Base):
    __tablename__ = "project_summaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class FundingCallRow(Base):
    __tablename__ = "funding_calls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String(128))
    institution = Column(String(256), nullable=True)
    call_title = Column(String(512))
    summary = Column(Text, nullable=True)
    deadline = Column(String(64), nullable=True)
    funding_amount = Column(String(128), nullable=True)
    funding_rate = Column(String(64), nullable=True)
    project_duration = Column(String(64), nullable=True)
    eligible_applicants = Column(Text, default="[]")
    eligible_countries = Column(Text, default="[]")
    technology_areas = Column(Text, default="[]")
    sectors = Column(Text, default="[]")
    trl_min = Column(Integer, nullable=True)
    trl_max = Column(Integer, nullable=True)
    consortium_required = Column(Boolean, nullable=True)
    application_url = Column(String(1024), nullable=True)
    guide_url = Column(String(1024), nullable=True)
    source_url = Column(String(1024))
    raw_text = Column(Text, nullable=True)
    extracted_at = Column(String(64), nullable=True)
    verification_status = Column(String(64), default="doğrulanmalı")


class MatchResultRow(Base):
    __tablename__ = "match_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    call_title = Column(String(512))
    source_name = Column(String(128))
    institution = Column(String(256), nullable=True)
    matched_user_type = Column(String(32))
    total_score = Column(Integer)
    status = Column(String(64))
    strengths = Column(Text, default="[]")
    weaknesses = Column(Text, default="[]")
    risks = Column(Text, default="[]")
    missing_documents = Column(Text, default="[]")
    required_checks = Column(Text, default="[]")
    recommended_action = Column(Text, default="")
    project_revision_suggestions = Column(Text, default="[]")
    deadline = Column(String(64), nullable=True)
    source_url = Column(String(1024))
    funding_amount = Column(String(128), nullable=True)
    funding_rate = Column(String(64), nullable=True)
    application_url = Column(String(1024), nullable=True)
    guide_url = Column(String(1024), nullable=True)
    explanation = Column(Text, nullable=True)
    subscores = Column(Text, default="{}")


def init_db() -> None:
    """Tabloları oluşturur (yoksa)."""
    Base.metadata.create_all(engine)


def get_session():
    """Yeni bir veritabanı oturumu döndürür."""
    return SessionLocal()


# --------------------------------------------------------------------------
# JSON yardımcıları
# --------------------------------------------------------------------------
def dumps(value) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)


def loads(value: Optional[str], default):
    if not value:
        return default
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default
