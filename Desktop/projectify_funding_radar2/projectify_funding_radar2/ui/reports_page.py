"""Raporlar — Excel / PDF indir (başvuran + proje bilgileri ve künye dahil)."""
from __future__ import annotations

import streamlit as st

from reports import export_results_to_excel, export_results_to_pdf
from services import list_results, load_profile, load_project_summary


def render():
    st.subheader("📑 Raporlar")
    results = list_results()
    if not results:
        st.info("İndirilecek sonuç yok. Önce tarama ve eşleştirme yapın.")
        return

    user_type, profile = load_profile()
    project = load_project_summary()

    st.write(f"Toplam **{len(results)}** sonuç dışa aktarılabilir. "
             "Raporlar başvuran bilgilerini, proje özetini ve Pi Sağlık Teknolojileri künyesini içerir.")
    c1, c2 = st.columns(2)

    xlsx = export_results_to_excel(results, user_type=user_type, profile=profile, project=project)
    c1.download_button(
        "⬇️ Excel (.xlsx) indir", data=xlsx,
        file_name="funding_radar_sonuclar.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    data, ext = export_results_to_pdf(results, user_type=user_type, profile=profile, project=project)
    mime = "application/pdf" if ext == "pdf" else "text/plain"
    c2.download_button(
        f"⬇️ Rapor (.{ext}) indir", data=data,
        file_name=f"funding_radar_rapor.{ext}", mime=mime,
    )
