"""Tarama ve Analiz — tarama başlat, eşleştir, Clear/Taramaları Sil."""
from __future__ import annotations

import streamlit as st

from config import USER_TYPE_LABELS
from services import (CONFIRM_TEXT, clear_scan_results, count_calls, count_results,
                      has_profile, load_project_summary, run_matching, scan_and_store)
from sources import READY_SOURCES


def render():
    st.subheader("🔍 Tarama ve Analiz")

    profile_ok = has_profile()
    project_ok = load_project_summary() is not None
    if not (profile_ok and project_ok):
        st.warning("Tarama öncesi **Kullanıcı Profili** ve **Proje Özeti** tamamlanmalı.")

    c1, c2 = st.columns(2)
    c1.metric("Taranan Çağrı", count_calls())
    c2.metric("Skorlanan Sonuç", count_results())

    use_live = st.toggle("Canlı scraping dene (başarısız olursa demo veriye düşer)", value=True)

    st.markdown("**Tarama**")
    selected = st.session_state.get("selected_sources", ["cascade"])
    st.write("Seçili kaynaklar:", ", ".join(READY_SOURCES[k] for k in selected) or "—")

    cc1, cc2 = st.columns(2)
    if cc1.button("Tüm Seçili Kaynakları Tara", type="primary"):
        with st.spinner("Kaynaklar taranıyor..."):
            counts = scan_and_store(selected, use_live=use_live)
        st.success("Tarama tamamlandı: " + ", ".join(
            f"{READY_SOURCES[k]}: {n}" for k, n in counts.items()))

    if cc2.button("Eşleştir ve Skorla"):
        if not (profile_ok and project_ok):
            st.error("Profil ve proje özeti gerekli.")
        else:
            with st.spinner("Uygunluk skorları hesaplanıyor..."):
                results = run_matching()
            st.success(f"{len(results)} çağrı skorlandı. **Uygunluk Sonuçları** sayfasına geçin.")

    st.divider()
    st.markdown("### 🗑️ Clear / Taramaları Sil")
    st.caption(CONFIRM_TEXT)
    confirm = st.checkbox("Yukarıdaki uyarıyı okudum ve onaylıyorum.")
    if st.button("Taramaları Sil", disabled=not confirm):
        res = clear_scan_results()
        st.success(
            f"Silindi → çağrı: {res['calls_deleted']}, sonuç: {res['results_deleted']}. "
            "Profil ve proje özeti korundu."
        )
