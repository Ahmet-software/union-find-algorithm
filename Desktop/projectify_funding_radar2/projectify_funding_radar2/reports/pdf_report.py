"""
PDF rapor üretimi — fitz.Story (HTML) ile.
İçerir: logo başlığı, başvuran bilgileri, proje özeti, uygunluk sonuçları
ve her sayfada künye (Pi Sağlık Teknolojileri / pixr.store).
PyMuPDF yoksa düz metin (.txt) döner.
"""
from __future__ import annotations

import html
import io
from typing import List, Optional, Tuple

from config import (DEVELOPER_LINE, DEVELOPER_WEBSITE, LOGO_PATH,
                    PROFILE_FIELD_LABELS, USER_TYPE_LABELS)
from matcher.score_explainer import generate_match_explanation
from models import MatchResult

_PROJECT_LABELS = {
    "project_name": "Proje Adı", "project_purpose": "Proje Amacı",
    "project_rationale": "Proje Gerekçesi", "project_method": "Proje Yöntemi",
    "commercialization_patent_status": "Ticarileşme ve Patentlenebilirlik",
    "competitors": "Rakipler", "competitive_advantage": "Rekabet Avantajı",
}


def _esc(s) -> str:
    return html.escape(str(s)) if s is not None else "-"


def _ul(title: str, items: List[str]) -> str:
    if not items:
        return ""
    lis = "".join(f"<p class='li'>• {_esc(it)}</p>" for it in items)
    return f"<p class='lbl'>{title}</p>{lis}"


def build_report_text(results: List[MatchResult]) -> str:
    lines = ["PROJECTIFY FUNDING RADAR - UYGUNLUK RAPORU", "=" * 50, ""]
    for i, r in enumerate(results, start=1):
        lines.append(f"{i}. {r.call_title}  ({r.source_name})")
        lines.append("-" * 50)
        lines.append(generate_match_explanation(r))
        lines.append("")
    lines.append("")
    lines.append(DEVELOPER_LINE + "  " + DEVELOPER_WEBSITE)
    return "\n".join(lines)


def _profile_html(user_type, profile) -> str:
    if not (user_type and profile):
        return ""
    data = profile.model_dump()
    rows = []
    for key, val in data.items():
        if val in (None, "", [], 0, 0.0):
            continue
        label = PROFILE_FIELD_LABELS.get(key, key)
        if isinstance(val, list):
            val = ", ".join(str(v) for v in val)
        if isinstance(val, bool):
            val = "Evet" if val else "Hayir"
        rows.append(f"<p class='kv'><b>{_esc(label)}:</b> {_esc(val)}</p>")
    if not rows:
        return ""
    tlabel = USER_TYPE_LABELS.get(user_type, user_type)
    return (f"<p class='sec'>Başvuran Bilgileri — {_esc(tlabel)}</p>"
            f"<div class='info'>{''.join(rows)}</div>")


def _project_html(project) -> str:
    if not project:
        return ""
    data = project.model_dump()
    rows = []
    for key, label in _PROJECT_LABELS.items():
        val = data.get(key, "")
        if not val:
            continue
        rows.append(f"<p class='kv'><b>{_esc(label)}:</b> {_esc(val)}</p>")
    if not rows:
        return ""
    return f"<p class='sec'>Proje Özeti</p><div class='info'>{''.join(rows)}</div>"


def _results_html(results) -> str:
    blocks = []
    for i, r in enumerate(results, start=1):
        color = {
            "Çok Uygun": "#1a9850", "Uygun": "#66bd63", "Revizyonla Uygun": "#fdae61",
            "Düşük Uygunluk": "#f46d43", "Uygun Değil": "#d73027",
        }.get(r.status, "#555")
        meta = (
            f"<b>Kaynak:</b> {_esc(r.source_name)} &nbsp;|&nbsp; "
            f"<b>Kurum:</b> {_esc(r.institution)} &nbsp;|&nbsp; "
            f"<b>Tip:</b> {_esc(USER_TYPE_LABELS.get(r.matched_user_type, r.matched_user_type))} &nbsp;|&nbsp; "
            f"<b>Son tarih:</b> {_esc(r.deadline)}"
        )
        funding = (f"<b>Destek:</b> {_esc(r.funding_amount)} / oran {_esc(r.funding_rate)}"
                   if (r.funding_amount or r.funding_rate) else "")
        link = (f"<p class='meta'><b>Bağlantı:</b> {_esc(r.application_url or r.source_url)}</p>"
                if (r.application_url or r.source_url) else "")
        blocks.append(f"""
        <div class="card">
          <p class="title">{i}. {_esc(r.call_title)}</p>
          <p class="score" style="color:{color}">{r.total_score}/100 — {_esc(r.status)}</p>
          <p class="meta">{meta}</p>
          {f'<p class="meta">{funding}</p>' if funding else ''}
          {_ul("Güçlü yönler", r.strengths)}
          {_ul("Zayıf yönler", r.weaknesses)}
          {_ul("Riskler", r.risks)}
          {_ul("Eksik belgeler", r.missing_documents)}
          {_ul("Doğrulanması gerekenler", r.required_checks)}
          {_ul("Revizyon önerileri", r.project_revision_suggestions)}
          <p class="lbl">Önerilen ilk aksiyon</p>
          <p class="action">{_esc(r.recommended_action)}</p>
          {link}
        </div>""")
    return "".join(blocks)


def _build_html(results, user_type, profile, project) -> str:
    logo_tag = '<img src="logo.png" width="190" />' if LOGO_PATH.exists() else ""
    return f"""
    <html><head><style>
      * {{ font-family: sans-serif; }}
      h1 {{ color:#0b2e59; font-size:17px; margin:6px 0 2px 0; }}
      .subtitle {{ color:#2a7f8e; font-size:11px; margin:0 0 8px 0; }}
      .sec {{ color:#fff; background:#0b2e59; font-size:12px; font-weight:bold;
              padding:4px 8px; border-radius:4px; margin:10px 0 4px 0; }}
      .info {{ margin-bottom:6px; }}
      .kv {{ font-size:9.8px; color:#333; margin:0; padding:3px 6px;
             border-bottom:1px solid #e6ecf2; }}
      .kv b {{ color:#0b2e59; }}
      .card {{ border:1px solid #d9e2ec; border-radius:6px; padding:8px 10px; margin-bottom:10px; }}
      .title {{ font-size:13px; font-weight:bold; color:#0b2e59; margin:0 0 2px 0; }}
      .score {{ font-size:13px; font-weight:bold; margin:0 0 4px 0; }}
      .meta {{ font-size:9.5px; color:#444; margin:1px 0; }}
      .lbl {{ font-size:10px; font-weight:bold; color:#0b2e59; margin:6px 0 1px 0; }}
      .li {{ font-size:9.5px; color:#333; margin:0 0 0 10px; }}
      .action {{ font-size:10px; color:#1a5276; margin:0; }}
    </style></head><body>
      <div>{logo_tag}</div>
      <h1>Uygunluk Raporu</h1>
      <p class="subtitle">Projectify Funding Radar — Toplam {len(results)} sonuç</p>
      {_profile_html(user_type, profile)}
      {_project_html(project)}
      <p class="sec">Uygunluk Sonuçları</p>
      {_results_html(results)}
    </body></html>
    """


def _stamp_footer(pdf_bytes: bytes) -> bytes:
    try:
        import fitz
    except ImportError:
        return pdf_bytes
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        n = doc.page_count
        footer_html = (
            f"<div style='font-family:sans-serif;text-align:center;font-size:8px;color:#777;'>"
            f"{html.escape(DEVELOPER_LINE)} &nbsp;|&nbsp; "
            f"<b style='color:#00838f'>{html.escape(DEVELOPER_WEBSITE)}</b></div>"
        )
        for i, page in enumerate(doc, start=1):
            w, h = page.rect.width, page.rect.height
            page.draw_line(fitz.Point(40, h - 42), fitz.Point(w - 40, h - 42),
                           color=(0.85, 0.88, 0.92), width=0.7)
            try:
                page.insert_htmlbox(fitz.Rect(40, h - 40, w - 40, h - 22), footer_html)
            except Exception:
                pass
            try:
                page.insert_textbox(fitz.Rect(w - 95, h - 40, w - 40, h - 26),
                                    f"{i}/{n}", fontsize=7.5, color=(0.5, 0.5, 0.5), align=2)
            except Exception:
                pass
        out = doc.tobytes()
        doc.close()
        return out
    except Exception:
        return pdf_bytes


def export_results_to_pdf(results, user_type=None, profile=None, project=None) -> Tuple[bytes, str]:
    if not results:
        return build_report_text(results).encode("utf-8"), "txt"
    try:
        import fitz

        html_str = _build_html(results, user_type, profile, project)
        buf = io.BytesIO()
        writer = fitz.DocumentWriter(buf)
        archive = fitz.Archive(str(LOGO_PATH.parent)) if LOGO_PATH.exists() else None
        story = fitz.Story(html=html_str, archive=archive)
        mediabox = fitz.paper_rect("a4")
        where = mediabox + (40, 40, -40, -52)
        more = 1
        while more:
            dev = writer.begin_page(mediabox)
            more, _ = story.place(where)
            story.draw(dev)
            writer.end_page()
        writer.close()
        data = _stamp_footer(buf.getvalue())
        if len(data) < 800:
            return build_report_text(results).encode("utf-8"), "txt"
        return data, "pdf"
    except Exception:
        return build_report_text(results).encode("utf-8"), "txt"
