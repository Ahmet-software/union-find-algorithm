"""Akademisyen profil formu — doküman bölüm 4 & 11."""
from __future__ import annotations

import streamlit as st

from models import AcademicProfile
from services import save_profile


def render():
    st.subheader("🎓 Akademisyen Profili")
    with st.form("academic_form"):
        c1, c2 = st.columns(2)
        full_name = c1.text_input("Ad soyad *")
        university = c2.text_input("Üniversite *")
        faculty = c1.text_input("Fakülte")
        department = c2.text_input("Bölüm")
        division = c1.text_input("Ana bilim dalı")
        academic_title = c2.text_input("Akademik unvan")

        expertise = st.text_input("Uzmanlık alanları (virgülle ayırın)")
        previous_projects = st.text_area("Daha önce yürüttüğü projeler", height=70)
        publications = st.text_area("Yayın bilgileri", height=70)
        patents = st.text_input("Patent / faydalı model bilgileri")

        l1, l2 = st.columns(2)
        laboratory_infrastructure = l1.text_input("Laboratuvar / araştırma altyapısı")
        tto_info = l2.text_input("Üniversite TTO bilgisi")
        ethics = l1.selectbox("Etik kurul / klinik araştırma altyapısı", ["", "Var", "Yok"])
        industry = l2.text_input("Sanayi iş birliği geçmişi")

        uploaded = st.file_uploader("Özgeçmiş / belgeler (PDF)", accept_multiple_files=True)
        submitted = st.form_submit_button("Profili Kaydet", type="primary")

    if submitted:
        if not full_name.strip() or not university.strip():
            st.error("Ad soyad ve üniversite zorunludur.")
            return
        profile = AcademicProfile(
            full_name=full_name.strip(),
            university=university.strip(),
            faculty=faculty or None,
            department=department or None,
            division=division or None,
            academic_title=academic_title or None,
            expertise_fields=[e.strip() for e in expertise.split(",") if e.strip()],
            previous_projects=previous_projects or None,
            publications=publications or None,
            patents=patents or None,
            laboratory_infrastructure=laboratory_infrastructure or None,
            tto_info=tto_info or None,
            ethics_committee_access=ethics or None,
            industry_collaboration_history=industry or None,
            uploaded_documents=[f.name for f in uploaded] if uploaded else [],
        )
        save_profile("academic", profile)
        st.success("✅ Akademisyen profili kaydedildi.")
