"""
semantic_matcher.py
MVP'de hafif (kelime örtüşmesi tabanlı) semantik benzerlik.
v2'de sentence-transformers ile değiştirilebilir (doküman bölüm 34).
"""
from __future__ import annotations

from extractors.text_cleaner import normalize_for_match


def semantic_similarity(text_a: str, text_b: str) -> float:
    """0..1 arası kaba benzerlik (Jaccard kelime örtüşmesi)."""
    a = set(normalize_for_match(text_a).split())
    b = set(normalize_for_match(text_b).split())
    a = {w for w in a if len(w) > 3}
    b = {w for w in b if len(w) > 3}
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0
