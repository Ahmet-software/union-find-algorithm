"""Excel rapor üretimi — doküman bölüm 31 kolonları."""
from __future__ import annotations

import io
from typing import List

from models import MatchResult

COLUMNS = [
    "Sıra No", "Program Adı", "Kaynak", "Kurum", "Kullanıcı Tipi",
    "Uygunluk Skoru", "Uygunluk Seviyesi", "Son Başvuru Tarihi",
    "Destek Miktarı", "Destek Oranı", "Güçlü Yönler", "Zayıf Yönler",
    "Riskler", "Eksik Belgeler", "Önerilen Aksiyon", "Başvuru Linki", "Rehber Linki",
]

_TYPE_TR = {"company": "Şirket", "academic": "Akademisyen", "entrepreneur": "Girişimci"}


def _join(items: List[str]) -> str:
    return " | ".join(items) if items else "-"


def export_results_to_excel(results: List[MatchResult], user_type=None, profile=None, project=None) -> bytes:
    """Sonuçları .xlsx içeriği (bytes) olarak döndürür. Profil/proje varsa ikinci sayfaya yazar."""
    try:
        import pandas as pd
    except ImportError:
        return _export_with_openpyxl(results)

    rows = []
    for i, r in enumerate(results, start=1):
        rows.append({
            "Sıra No": i,
            "Program Adı": r.call_title,
            "Kaynak": r.source_name,
            "Kurum": r.institution or "-",
            "Kullanıcı Tipi": _TYPE_TR.get(r.matched_user_type, r.matched_user_type),
            "Uygunluk Skoru": r.total_score,
            "Uygunluk Seviyesi": r.status,
            "Son Başvuru Tarihi": r.deadline or "-",
            "Destek Miktarı": r.funding_amount or "-",
            "Destek Oranı": r.funding_rate or "-",
            "Güçlü Yönler": _join(r.strengths),
            "Zayıf Yönler": _join(r.weaknesses),
            "Riskler": _join(r.risks),
            "Eksik Belgeler": _join(r.missing_documents),
            "Önerilen Aksiyon": r.recommended_action or "-",
            "Başvuru Linki": r.application_url or r.source_url or "-",
            "Rehber Linki": r.guide_url or "-",
        })
    df = pd.DataFrame(rows, columns=COLUMNS)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Uygunluk Sonuçları")
        ws = writer.sheets["Uygunluk Sonuçları"]
        for col_idx, col in enumerate(COLUMNS, start=1):
            ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = min(
                45, max(12, len(col) + 4)
            )
        # İkinci sayfa: Başvuran & Proje bilgileri
        info_rows = _info_rows(user_type, profile, project)
        if info_rows:
            idf = pd.DataFrame(info_rows, columns=["Bölüm", "Alan", "Değer"])
            idf.to_excel(writer, index=False, sheet_name="Başvuran & Proje")
            iws = writer.sheets["Başvuran & Proje"]
            iws.column_dimensions["A"].width = 22
            iws.column_dimensions["B"].width = 28
            iws.column_dimensions["C"].width = 70
    return buf.getvalue()


def _info_rows(user_type, profile, project):
    from config import PROFILE_FIELD_LABELS, USER_TYPE_LABELS
    out = []
    if user_type and profile:
        section = f"Başvuran ({USER_TYPE_LABELS.get(user_type, user_type)})"
        for k, v in profile.model_dump().items():
            if v in (None, "", [], 0, 0.0):
                continue
            if isinstance(v, list):
                v = ", ".join(str(x) for x in v)
            if isinstance(v, bool):
                v = "Evet" if v else "Hayır"
            out.append([section, PROFILE_FIELD_LABELS.get(k, k), str(v)])
    if project:
        plabels = {
            "project_name": "Proje Adı", "project_purpose": "Proje Amacı",
            "project_rationale": "Proje Gerekçesi", "project_method": "Proje Yöntemi",
            "commercialization_patent_status": "Ticarileşme ve Patentlenebilirlik",
            "competitors": "Rakipler", "competitive_advantage": "Rekabet Avantajı",
        }
        for k, label in plabels.items():
            v = project.model_dump().get(k, "")
            if v:
                out.append(["Proje Özeti", label, str(v)])
    return out


def _export_with_openpyxl(results: List[MatchResult]) -> bytes:
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "Uygunluk Sonuçları"
    ws.append(COLUMNS)
    for i, r in enumerate(results, start=1):
        ws.append([
            i, r.call_title, r.source_name, r.institution or "-",
            _TYPE_TR.get(r.matched_user_type, r.matched_user_type),
            r.total_score, r.status, r.deadline or "-",
            r.funding_amount or "-", r.funding_rate or "-",
            _join(r.strengths), _join(r.weaknesses), _join(r.risks),
            _join(r.missing_documents), r.recommended_action or "-",
            r.application_url or "-", r.guide_url or "-",
        ])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
