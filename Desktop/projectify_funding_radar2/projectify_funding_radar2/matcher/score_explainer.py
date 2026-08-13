"""
score_explainer.py
MatchResult'tan insan-okunur açıklama metni üretir (doküman bölüm 20 & 30).
"""
from __future__ import annotations

from models import MatchResult


def generate_match_explanation(result: MatchResult) -> str:
    lines = []
    lines.append(f"Skor: {result.total_score}/100 — {result.status}")
    lines.append("")
    if result.strengths:
        lines.append("Neden uygun / güçlü yönler:")
        lines += [f"  • {s}" for s in result.strengths]
        lines.append("")
    if result.weaknesses:
        lines.append("Zayıf yönler:")
        lines += [f"  • {w}" for w in result.weaknesses]
        lines.append("")
    if result.risks:
        lines.append("Riskler:")
        lines += [f"  • {r}" for r in result.risks]
        lines.append("")
    if result.missing_documents:
        lines.append("Eksik belgeler:")
        lines += [f"  • {m}" for m in result.missing_documents]
        lines.append("")
    if result.required_checks:
        lines.append("Doğrulanması gereken bilgiler:")
        lines += [f"  • {c}" for c in result.required_checks]
        lines.append("")
    if result.project_revision_suggestions:
        lines.append("Proje revizyon önerileri:")
        lines += [f"  • {p}" for p in result.project_revision_suggestions]
        lines.append("")
    lines.append(f"Önerilen ilk aksiyon: {result.recommended_action}")
    return "\n".join(lines)
