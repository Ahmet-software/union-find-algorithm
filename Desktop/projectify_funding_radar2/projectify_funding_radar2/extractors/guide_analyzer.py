"""
guide_analyzer.py
Ham metinden (PDF / web / manuel) standart FundingCall üretir.

extract_funding_call_from_text: kural tabanlı çıkarım. Emin olunamayan
alanlar 'doğrulanmalı' olarak işaretlenir (verification_status).
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from extractors.date_extractor import extract_deadline
from extractors.eligibility_extractor import (
    detect_consortium,
    extract_countries,
    extract_eligible_applicants,
    extract_sectors,
    extract_technologies,
)
from extractors.funding_amount_extractor import (
    extract_duration,
    extract_funding_amount,
    extract_funding_rate,
    extract_trl,
)
from extractors.text_cleaner import clean_text, first_nonempty_line
from models import FundingCall


def extract_funding_call_from_text(
    raw_text: str,
    source_name: str = "Manuel/Yüklenen",
    source_url: str = "manual://uploaded",
    institution: Optional[str] = None,
    call_title: Optional[str] = None,
) -> FundingCall:
    text = clean_text(raw_text or "")
    title = call_title or first_nonempty_line(text)[:200] or "İsimsiz Çağrı"

    trl_min, trl_max = extract_trl(text)
    applicants = extract_eligible_applicants(text)
    sectors = extract_sectors(text)
    techs = extract_technologies(text)
    countries = extract_countries(text)
    deadline = extract_deadline(text)
    amount = extract_funding_amount(text)
    rate = extract_funding_rate(text)
    duration = extract_duration(text)
    consortium = detect_consortium(text)

    # Kritik alanların kaçı bulunabildi? Çok azsa 'doğrulanmalı' kalır.
    found = sum(
        1
        for v in [applicants, sectors, techs, deadline, amount, trl_min]
        if v
    )
    verification = "doğrulandı" if found >= 4 else "doğrulanmalı"

    return FundingCall(
        source_name=source_name,
        institution=institution,
        call_title=title,
        summary=text[:500] if text else None,
        deadline=deadline,
        funding_amount=amount,
        funding_rate=rate,
        project_duration=duration,
        eligible_applicants=applicants,
        eligible_countries=countries,
        technology_areas=techs,
        sectors=sectors,
        trl_min=trl_min,
        trl_max=trl_max,
        consortium_required=consortium,
        application_url=source_url if source_url and source_url.startswith('http') else None,
        source_url=source_url,
        raw_text=text[:5000],
        extracted_at=datetime.utcnow().isoformat(timespec="seconds"),
        verification_status=verification,
    )
