"""Proje Özeti formu — doküman bölüm 6. Her alan ≤ 500 karakter + canlı sayaç."""
from __future__ import annotations

import os
import tempfile

import streamlit as st

from config import PROJECT_SUMMARY_MAX_LEN
from extractors import extract_text_from_pdf
from models import ProjectSummary
from services import field_labels, load_project_summary, save_project_summary, validate_project_summary

_MAX = PROJECT_SUMMARY_MAX_LEN
_FIELDS = list(field_labels().items())


def _counter(value: str):
    n = len(value or "")
    color = "red" if n > _MAX else ("orange" if n > _MAX * 0.9 else "gray")
    st.markdown(
        f"<span style='color:{color};font-size:0.8em'>{n} / {_MAX} karakter</span>",
        unsafe_allow_html=True,
    )


def render():
    st.subheader("📝 Proje Özeti")
    tab_manual, tab_pdf = st.tabs(["Manuel giriş", "PDF yükle"])

    existing = load_project_summary()
    defaults = existing.model_dump() if existing else {}

    with tab_pdf:
        st.caption("Proje özetinizi PDF olarak yükleyin; metin çıkarılıp Proje Adı'na ön-doldurulur.")
        up = st.file_uploader("Proje özeti PDF", type=["pdf"], key="proj_pdf")
        if up is not None:
            fd, path = tempfile.mkstemp(suffix=".pdf")
            with os.fdopen(fd, "wb") as f:
                f.write(up.read())
            text = extract_text_from_pdf(path)
            os.unlink(path)
            if text:
                st.text_area("Çıkarılan metin (önizleme)", text[:2000], height=200)
                st.info("Metni aşağıdaki alanlara kopyalayıp 500 karakter sınırına göre düzenleyin.")
            else:
                st.warning("PDF'ten metin çıkarılamadı (PyMuPDF kurulu değil veya metin yok).")

    with tab_manual:
        values = {}
        with st.form("project_form"):
            for field, label in _FIELDS:
                values[field] = st.text_area(f"{label} *", value=defaults.get(field, ""), height=80, key=f"f_{field}")
                _counter(values[field])
            submitted = st.form_submit_button("Proje Özetini Kaydet", type="primary")

        if submitted:
            ok, errors = validate_project_summary(values)
            if not ok:
                st.error("Form kaydedilmedi — 500 karakter sınırı aşıldı:")
                for e in errors:
                    st.write(f"• {e}")
                return
            if not values["project_name"].strip():
                st.error("Proje Adı zorunludur.")
                return
            save_project_summary(ProjectSummary(**values))
            st.success("✅ Proje özeti kaydedildi.")
