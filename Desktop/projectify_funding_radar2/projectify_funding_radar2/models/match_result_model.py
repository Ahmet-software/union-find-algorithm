"""Eşleşme sonucu veri modeli — doküman bölüm 13."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class MatchResult(BaseModel):
    id: Optional[int] = None

    call_title: str
    source_name: str
    institution: Optional[str] = None
    matched_user_type: str

    total_score: int
    status: str

    strengths: List[str] = []
    weaknesses: List[str] = []
    risks: List[str] = []
    missing_documents: List[str] = []
    required_checks: List[str] = []

    recommended_action: str = ""
    project_revision_suggestions: List[str] = []

    deadline: Optional[str] = None
    source_url: str

    # Ek görsel alanlar (dashboard için pratiklik)
    funding_amount: Optional[str] = None
    funding_rate: Optional[str] = None
    application_url: Optional[str] = None
    guide_url: Optional[str] = None
    explanation: Optional[str] = None
    subscores: dict = {}
