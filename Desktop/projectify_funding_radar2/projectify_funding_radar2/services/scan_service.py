"""Fon kaynaklarını tarar ve çağrıları veritabanına kaydeder."""
from __future__ import annotations

from typing import Dict, List

from database import FundingCallRow, get_session
from config import is_active_call
from models import FundingCall
from services._mappers import call_to_row, row_to_call
from sources import scan_sources


def _active_only(calls):
    """Son başvuru tarihi geçmiş çağrıları eler (tarihi bilinmeyenler kalır)."""
    return [c for c in calls if is_active_call(c.deadline)]


def scan_and_store(source_keys: List[str], use_live: bool = True) -> Dict[str, int]:
    """Kaynakları tarar, geçmiş tarihlileri eleyip çağrıları kaydeder. {kaynak: eklenen_adet}."""
    results = scan_sources(source_keys, use_live=use_live)
    counts: Dict[str, int] = {}
    with get_session() as s:
        for key, calls in results.items():
            active = _active_only(calls)
            for call in active:
                s.add(call_to_row(call))
            counts[key] = len(active)
        s.commit()
    return counts


def store_calls(calls: List[FundingCall]) -> int:
    active = _active_only(calls)
    with get_session() as s:
        for call in active:
            s.add(call_to_row(call))
        s.commit()
    return len(active)


def list_calls() -> List[FundingCall]:
    with get_session() as s:
        rows = s.query(FundingCallRow).order_by(FundingCallRow.id.desc()).all()
        return [row_to_call(r) for r in rows]


def count_calls() -> int:
    with get_session() as s:
        return s.query(FundingCallRow).count()
