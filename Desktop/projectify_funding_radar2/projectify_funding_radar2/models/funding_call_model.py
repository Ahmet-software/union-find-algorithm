"""Çağrı (FundingCall) veri modeli — doküman bölüm 8."""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class FundingCall(BaseModel):
    id: Optional[int] = None
    source_name: str
    institution: Optional[str] = None
    call_title: str
    summary: Optional[str] = None

    deadline: Optional[date] = None
    funding_amount: Optional[str] = None
    funding_rate: Optional[str] = None
    project_duration: Optional[str] = None

    eligible_applicants: List[str] = []
    eligible_countries: List[str] = []
    technology_areas: List[str] = []
    sectors: List[str] = []

    trl_min: Optional[int] = None
    trl_max: Optional[int] = None
    consortium_required: Optional[bool] = None

    application_url: Optional[str] = None
    guide_url: Optional[str] = None
    source_url: str

    raw_text: Optional[str] = None
    extracted_at: Optional[str] = None
    verification_status: Optional[str] = "doğrulanmalı"
