"""Girişimci profili veri modeli — doküman bölüm 12."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class EntrepreneurProfile(BaseModel):
    full_name: str
    education_level: Optional[str] = None
    university: Optional[str] = None
    faculty: Optional[str] = None
    department: Optional[str] = None
    graduation_status: Optional[str] = None

    startup_idea_name: Optional[str] = None
    previous_projects: Optional[str] = None
    trainings_certificates: Optional[str] = None

    team_members: Optional[str] = None
    has_technical_team: Optional[bool] = None
    has_business_team: Optional[bool] = None

    project_stage: Optional[str] = None
    company_establishment_plan: Optional[str] = None
    patent_or_brand_status: Optional[str] = None
    prototype_status: Optional[str] = None
    customer_validation_status: Optional[str] = None
    sales_or_loi_status: Optional[str] = None
