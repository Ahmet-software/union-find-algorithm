"""Fon Kaynakları — hazır kaynaklar, yeni site, yeni PDF rehber, manuel program."""
from __future__ import annotations

import os
import tempfile

import streamlit as st

from config import is_active_call
from extractors import extract_funding_call_from_text
from services import analyze_and_match, analyze_guide_url, analyze_uploaded_guide
from sources import READY_SOURCES


def _add_if_active(call):
    """Geçmiş tarihli çağrıyı eklemez; uyarır. Aktifse ekleyip eşleştirir."""
    if not is_active_call(call.deadline):
        st.warning(
            f"Bu çağrının son başvuru tarihi geçmiş ({call.deadline}). "
            "Geçmiş tarihli çağrılar eklenmez."
        )
        return None
    _, result = analyze_and_match(call)
    return result


def render():
    st.subheader("💰 Fon Kaynakları")
    t1, t2, t3, t4 = st.tabs(
        ["Hazır kaynaklar", "Yeni site ekle", "Yeni PDF rehber ekle", "Manuel program ekle"]
    )

    with t1:
        st.caption("MVP'de **Cascade Funding** canlı taranır (yedek: demo veri). Diğerleri v2 stub'dur.")
        selected = st.multiselect(
            "Taranacak kaynaklar",
            options=list(READY_SOURCES.keys()),
            default=["cascade"],
            format_func=lambda k: READY_SOURCES[k],
        )
        st.session_state["selected_sources"] = selected
        st.info("Seçimi kaydettiniz. Taramayı **Tarama ve Analiz** sayfasından başlatın.")

    with t2:
        url = st.text_input("Program / çağrı web linki", placeholder="https://...")
        dynamic = st.checkbox("Dinamik (JS) sayfa — Playwright kullan")
        if st.button("Linki Analiz Et", key="url_btn") and url.strip():
            with st.spinner("Sayfa ve varsa PDF rehberler okunuyor..."):
                call = analyze_guide_url(url.strip(), dynamic=dynamic)
                result = _add_if_active(call)
            if result is not None:
                st.success(f"Çağrı eklendi: {call.call_title}")
                _show_quick_result(result)

    with t3:
        up = st.file_uploader("Çağrı rehberi (PDF)", type=["pdf"], key="guide_pdf")
        if up is not None and st.button("PDF Rehberi Analiz Et", key="pdf_btn"):
            fd, path = tempfile.mkstemp(suffix=".pdf")
            with os.fdopen(fd, "wb") as f:
                f.write(up.read())
            with st.spinner("PDF analiz ediliyor..."):
                call = analyze_uploaded_guide(path, source_name=f"Yüklenen: {up.name}")
            os.unlink(path)
            result = _add_if_active(call)
            if result is not None:
                st.success(f"Rehber eklendi: {call.call_title}")
                _show_quick_result(result)

    with t4:
        with st.form("manual_program"):
            title = st.text_input("Program adı *")
            institution = st.text_input("Kurum")
            body = st.text_area(
                "Program metni (kimler başvurabilir, destek miktarı, TRL, son tarih, sektör...)",
                height=200,
            )
            submitted = st.form_submit_button("Programı Ekle ve Eşleştir", type="primary")
        if submitted and title.strip():
            call = extract_funding_call_from_text(
                body, source_name="Manuel Giriş", source_url="manual://entry",
                institution=institution or None, call_title=title.strip(),
            )
            result = _add_if_active(call)
            if result is not None:
                st.success(f"Program eklendi: {call.call_title}")
                _show_quick_result(result)


def _show_quick_result(result):
    if not result:
        st.warning("Eşleştirme için önce profil ve proje özeti kaydedilmeli.")
        return
    st.metric(f"Uygunluk: {result.status}", f"{result.total_score}/100")
    with st.expander("Açıklamayı gör"):
        st.text(result.explanation or "")
