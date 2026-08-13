"""Kayıtlı çağrıları aktif profil + proje özetiyle eşleştirir ve sonuçları saklar."""
from __future__ import annotations

from typing import List, Optional

from database import MatchResultRow, get_session
from matcher import match_user_project_to_call
from models import MatchResult
from services._mappers import result_to_row, row_to_result
from services.profile_service import load_profile
from services.project_service import load_project_summary
from services.scan_service import list_calls


def run_matching() -> List[MatchResult]:
    """
    Aktif profil + proje özeti ile tüm kayıtlı çağrıları eşleştirir.
    Önceki match_results temizlenir ve yeniden hesaplanır.
    """
    user_type, profile = load_profile()
    project = load_project_summary()
    if not (user_type and profile and project):
        raise RuntimeError("Eşleştirme için profil ve proje özeti gereklidir.")

    calls = list_calls()
    results: List[MatchResult] = []
    with get_session() as s:
        s.query(MatchResultRow).delete()  # taze hesap
        for call in calls:
            try:
                res = match_user_project_to_call(user_type, profile, project, call)
            except Exception:  # noqa: BLE001
                continue
            results.append(res)
            s.add(result_to_row(res))
        s.commit()
    results.sort(key=lambda r: r.total_score, reverse=True)
    return results


def match_single_call(call) -> Optional[MatchResult]:
    user_type, profile = load_profile()
    project = load_project_summary()
    if not (user_type and profile and project):
        return None
    res = match_user_project_to_call(user_type, profile, project, call)
    with get_session() as s:
        s.add(result_to_row(res))
        s.commit()
    return res


def list_results() -> List[MatchResult]:
    with get_session() as s:
        rows = s.query(MatchResultRow).order_by(MatchResultRow.total_score.desc()).all()
        return [row_to_result(r) for r in rows]


def count_results() -> int:
    with get_session() as s:
        return s.query(MatchResultRow).count()
