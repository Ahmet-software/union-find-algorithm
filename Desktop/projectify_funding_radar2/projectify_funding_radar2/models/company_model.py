"""Şirket profili veri modeli — doküman bölüm 10."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class CompanyProfile(BaseModel):
    company_name: str
    establishment_year: Optional[int] = None
    activity_area: Optional[str] = None
    nace_code: Optional[str] = None
    employee_count: Optional[int] = None
    sme_status: Optional[str] = None

    balance_sheet_summary: Optional[str] = None
    net_sales: Optional[float] = None
    total_assets: Optional[float] = None

    tax_debt_status: Optional[str] = None
    sgk_debt_status: Optional[str] = None

    r_and_d_history: Optional[str] = None
    patent_brand_info: Optional[str] = None
    export_info: Optional[str] = None
    investment_incentive_history: Optional[str] = None

    uploaded_documents: List[str] = []
