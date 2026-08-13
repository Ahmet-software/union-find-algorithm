"""Pydantic model <-> ORM satır dönüşümleri."""
from __future__ import annotations

from datetime import date
from typing import List

from database import FundingCallRow, MatchResultRow, dumps, loads
from models import FundingCall, MatchResult


def call_to_row(call: FundingCall) -> FundingCallRow:
    return FundingCallRow(
        source_name=call.source_name,
        institution=call.institution,
        call_title=call.call_title,
        summary=call.summary,
        deadline=str(call.deadline) if call.deadline else None,
        funding_amount=call.funding_amount,
        funding_rate=call.funding_rate,
        project_duration=call.project_duration,
        eligible_applicants=dumps(call.eligible_applicants),
        eligible_countries=dumps(call.eligible_countries),
        technology_areas=dumps(call.technology_areas),
        sectors=dumps(call.sectors),
        trl_min=call.trl_min,
        trl_max=call.trl_max,
        consortium_required=call.consortium_required,
        application_url=call.application_url,
        guide_url=call.guide_url,
        source_url=call.source_url,
        raw_text=call.raw_text,
        extracted_at=call.extracted_at,
        verification_status=call.verification_status,
    )


def row_to_call(row: FundingCallRow) -> FundingCall:
    deadline = None
    if row.deadline:
        try:
            deadline = date.fromisoformat(row.deadline)
        except ValueError:
            deadline = None
    return FundingCall(
        id=row.id,
        source_name=row.source_name,
        institution=row.institution,
        call_title=row.call_title,
        summary=row.summary,
        deadline=deadline,
        funding_amount=row.funding_amount,
        funding_rate=row.funding_rate,
        project_duration=row.project_duration,
        eligible_applicants=loads(row.eligible_applicants, []),
        eligible_countries=loads(row.eligible_countries, []),
        technology_areas=loads(row.technology_areas, []),
        sectors=loads(row.sectors, []),
        trl_min=row.trl_min,
        trl_max=row.trl_max,
        consortium_required=row.consortium_required,
        application_url=row.application_url,
        guide_url=row.guide_url,
        source_url=row.source_url,
        raw_text=row.raw_text,
        extracted_at=row.extracted_at,
        verification_status=row.verification_status,
    )


def result_to_row(r: MatchResult) -> MatchResultRow:
    return MatchResultRow(
        call_title=r.call_title,
        source_name=r.source_name,
        institution=r.institution,
        matched_user_type=r.matched_user_type,
        total_score=r.total_score,
        status=r.status,
        strengths=dumps(r.strengths),
        weaknesses=dumps(r.weaknesses),
        risks=dumps(r.risks),
        missing_documents=dumps(r.missing_documents),
        required_checks=dumps(r.required_checks),
        recommended_action=r.recommended_action,
        project_revision_suggestions=dumps(r.project_revision_suggestions),
        deadline=r.deadline,
        source_url=r.source_url,
        funding_amount=r.funding_amount,
        funding_rate=r.funding_rate,
        application_url=r.application_url,
        guide_url=r.guide_url,
        explanation=r.explanation,
        subscores=dumps(r.subscores),
    )


def row_to_result(row: MatchResultRow) -> MatchResult:
    return MatchResult(
        id=row.id,
        call_title=row.call_title,
        source_name=row.source_name,
        institution=row.institution,
        matched_user_type=row.matched_user_type,
        total_score=row.total_score,
        status=row.status,
        strengths=loads(row.strengths, []),
        weaknesses=loads(row.weaknesses, []),
        risks=loads(row.risks, []),
        missing_documents=loads(row.missing_documents, []),
        required_checks=loads(row.required_checks, []),
        recommended_action=row.recommended_action or "",
        project_revision_suggestions=loads(row.project_revision_suggestions, []),
        deadline=row.deadline,
        source_url=row.source_url,
        funding_amount=row.funding_amount,
        funding_rate=row.funding_rate,
        application_url=row.application_url,
        guide_url=row.guide_url,
        explanation=row.explanation,
        subscores=loads(row.subscores, {}),
    )
