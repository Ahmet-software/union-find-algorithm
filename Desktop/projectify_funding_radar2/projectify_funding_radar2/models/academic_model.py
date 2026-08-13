"""Akademisyen profili veri modeli — doküman bölüm 11."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class AcademicProfile(BaseModel):
    full_name: str
    university: str
    faculty: Optional[str] = None
    department: Optional[str] = None
    division: Optional[str] = None
    academic_title: Optional[str] = None

    expertise_fields: List[str] = []
    previous_projects: Optional[str] = None
    publications: Optional[str] = None
    patents: Optional[str] = None

    laboratory_infrastructure: Optional[str] = None
    tto_info: Optional[str] = None
    ethics_committee_access: Optional[str] = None
    industry_collaboration_history: Optional[str] = None

    uploaded_documents: List[str] = []
