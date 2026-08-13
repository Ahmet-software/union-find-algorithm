"""Proje özeti doğrulama (500 karakter) + kaydet/yükle."""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from config import PROJECT_SUMMARY_MAX_LEN
from database import ProjectSummaryRow, dumps, get_session, loads
from models import ProjectSummary

_FIELD_LABELS = {
    "project_name": "Proje Adı",
    "project_purpose": "Proje Amacı",
    "project_rationale": "Proje Gerekçesi",
    "project_method": "Proje Yöntemi",
    "commercialization_patent_status": "Ticarileşme ve Patentlenebilirlik",
    "competitors": "Rakipler",
    "competitive_advantage": "Rekabet Avantajı",
}


def validate_project_summary(data: Dict[str, str]) -> Tuple[bool, List[str]]:
    """
    Doküman bölüm 24 — her alan en fazla 500 karakter.
    (ok, [aşan_alan_uyarıları]) döndürür.
    """
    errors: List[str] = []
    for field, label in _FIELD_LABELS.items():
        value = data.get(field, "") or ""
        if len(value) > PROJECT_SUMMARY_MAX_LEN:
            errors.append(
                f"'{label}' alanı {len(value)} karakter — sınır {PROJECT_SUMMARY_MAX_LEN}. "
                f"{len(value) - PROJECT_SUMMARY_MAX_LEN} karakter fazla."
            )
    return (len(errors) == 0), errors


def save_project_summary(project: ProjectSummary) -> None:
    with get_session() as s:
        s.query(ProjectSummaryRow).delete()
        s.add(ProjectSummaryRow(data_json=dumps(project.model_dump())))
        s.commit()


def load_project_summary() -> Optional[ProjectSummary]:
    with get_session() as s:
        row = s.query(ProjectSummaryRow).order_by(ProjectSummaryRow.id.desc()).first()
        if not row:
            return None
        return ProjectSummary(**loads(row.data_json, {}))


def field_labels() -> Dict[str, str]:
    return dict(_FIELD_LABELS)
