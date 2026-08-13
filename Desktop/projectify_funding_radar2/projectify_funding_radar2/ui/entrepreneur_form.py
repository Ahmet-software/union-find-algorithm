"""Girişimci profil formu — doküman bölüm 5 & 12."""
from __future__ import annotations

import streamlit as st

from models import EntrepreneurProfile
from services import save_profile

_STAGES = ["", "Fikir aşaması", "Ön doğrulama aşaması", "Prototip aşaması",
           "MVP aşaması", "Pilot uygulama aşaması"]


def render():
    st.subheader("🚀 Girişimci Profili")
    st.caption("Şirket kurulmadığı için vergi/SGK/bilanço gibi alanlar sorulmaz.")
    with st.form("entrepreneur_form"):
        c1, c2 = st.columns(2)
        full_name = c1.text_input("Ad soyad *")
        education_level = c2.text_input("Eğitim durumu")
        university = c1.text_input("Üniversite")
        faculty = c2.text_input("Fakülte / bölüm")
        graduation_status = c1.text_input("Mezuniyet durumu")
        startup_idea_name = c2.text_input("Girişim fikrinin adı")

        previous_projects = st.text_area("Daha önce yaptığı projeler", height=70)
        trainings = st.text_input("Aldığı eğitimler / sertifikalar")

        st.markdown("**Takım**")
        t1, t2, t3 = st.columns(3)
        team_members = t1.text_input("Takım üyeleri")
        has_technical_team = t2.checkbox("Teknik ekip var")
        has_business_team = t3.checkbox("İş geliştirme/satış ekibi var")

        st.markdown("**Proje aşaması ve olgunluk**")
        project_stage = st.selectbox("Proje hangi aşamada?", _STAGES)
        s1, s2 = st.columns(2)
        company_plan = s1.selectbox("Şirketleşme planı", ["", "Var", "Yok"])
        patent_status = s2.selectbox("Patent / marka başvurusu", ["", "Var", "Yok"])
        prototype_status = s1.selectbox("Prototip durumu", ["", "Var", "Yok"])
        customer_validation = s2.selectbox("Ön müşteri / kullanıcı görüşmesi", ["", "Yapıldı", "Yapılmadı"])
        sales_loi = st.selectbox("Satış veya niyet mektubu (LOI)", ["", "Var", "Yok"])

        submitted = st.form_submit_button("Profili Kaydet", type="primary")

    if submitted:
        if not full_name.strip():
            st.error("Ad soyad zorunludur.")
            return
        profile = EntrepreneurProfile(
            full_name=full_name.strip(),
            education_level=education_level or None,
            university=university or None,
            faculty=faculty or None,
            graduation_status=graduation_status or None,
            startup_idea_name=startup_idea_name or None,
            previous_projects=previous_projects or None,
            trainings_certificates=trainings or None,
            team_members=team_members or None,
            has_technical_team=has_technical_team,
            has_business_team=has_business_team,
            project_stage=project_stage or None,
            company_establishment_plan=company_plan or None,
            patent_or_brand_status=patent_status or None,
            prototype_status=prototype_status or None,
            customer_validation_status=customer_validation or None,
            sales_or_loi_status=sales_loi or None,
        )
        save_profile("entrepreneur", profile)
        st.success("✅ Girişimci profili kaydedildi.")
