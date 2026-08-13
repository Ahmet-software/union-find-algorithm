"""
guide_matcher.py
Kullanıcının yüklediği PDF/site/manuel program ile profil eşleştirmesi
(match_user_project_to_call'ı çağırır).
"""
from __future__ import annotations

from typing import Any

from models import FundingCall, MatchResult, ProjectSummary


def match_guide_to_profile(
    user_type: str, profile: Any, project: ProjectSummary, call: FundingCall
) -> MatchResult:
    from matcher import match_user_project_to_call

    return match_user_project_to_call(user_type, profile, project, call)
