"""Özet istatistik raporu (dashboard üst bilgisi için)."""
from __future__ import annotations

from typing import Dict, List

from models import MatchResult


def summarize(results: List[MatchResult]) -> Dict[str, int]:
    summary = {
        "total": len(results),
        "cok_uygun": 0, "uygun": 0, "revizyonla": 0, "dusuk": 0, "uygun_degil": 0,
    }
    for r in results:
        if r.status == "Çok Uygun":
            summary["cok_uygun"] += 1
        elif r.status == "Uygun":
            summary["uygun"] += 1
        elif r.status == "Revizyonla Uygun":
            summary["revizyonla"] += 1
        elif r.status == "Düşük Uygunluk":
            summary["dusuk"] += 1
        else:
            summary["uygun_degil"] += 1
    return summary
