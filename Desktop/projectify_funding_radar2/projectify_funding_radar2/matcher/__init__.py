"""matcher paketi — kullanıcı tipine göre doğru skorlayıcıyı seçer."""
from __future__ import annotations

from typing import Any

from matcher.academic_matcher import calculate_academic_match_score
from matcher.company_matcher import calculate_company_match_score
from matcher.entrepreneur_matcher import calculate_entrepreneur_match_score
from matcher.rule_based_score import classify_score
from matcher.score_explainer import generate_match_explanation
from models import FundingCall, MatchResult, ProjectSummary


def match_user_project_to_call(
    user_type: str, profile: Any, project: ProjectSummary, call: FundingCall
) -> MatchResult:
    """
    Doküman bölüm 24 — match_user_project_to_call.
    Kullanıcı tipi ne olursa olsun doğru matcher'ı seçip skor üretir.
    """
    if user_type == "company":
        result = calculate_company_match_score(profile, project, call)
    elif user_type == "academic":
        result = calculate_academic_match_score(profile, project, call)
    elif user_type == "entrepreneur":
        result = calculate_entrepreneur_match_score(profile, project, call)
    else:
        raise ValueError(f"Bilinmeyen kullanıcı tipi: {user_type}")

    result.explanation = generate_match_explanation(result)
    return result


__all__ = [
    "match_user_project_to_call",
    "calculate_company_match_score",
    "calculate_academic_match_score",
    "calculate_entrepreneur_match_score",
    "classify_score",
    "generate_match_explanation",
]
