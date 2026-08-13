"""Şirket profil formu — doküman bölüm 3 & 10."""
from __future__ import annotations

import streamlit as st

from models import CompanyProfile
from services import save_profile


def render():
    st.subheader("🏢 Şirket Profili")
    with st.form("company_form"):
        c1, c2 = st.columns(2)
        company_name = c1.text_input("Şirket unvanı *")
        establishment_year = c2.number_input("Kuruluş yılı", min_value=1900, max_value=2100, value=2020)
        activity_area = c1.text_input("Faaliyet alanı")
        nace_code = c2.text_input("NACE kodu")
        employee_count = c1.number_input("Personel sayısı", min_value=0, value=0)
        sme_status = c2.selectbox("KOBİ ölçeği", ["", "Mikro", "Küçük", "Orta", "Büyük"])

        st.markdown("**Finansal bilgiler**")
        f1, f2, f3 = st.columns(3)
        net_sales = f1.number_input("Net satış hasılatı (₺)", min_value=0.0, value=0.0)
        total_assets = f2.number_input("Aktif toplamı (₺)", min_value=0.0, value=0.0)
        balance_sheet_summary = f3.text_input("Bilanço özeti")

        st.markdown("**Risk / yükümlülük durumu**")
        r1, r2 = st.columns(2)
        tax_debt_status = r1.selectbox("Vergi borcu durumu", ["", "Yok", "Var"])
        sgk_debt_status = r2.selectbox("SGK borcu durumu", ["", "Yok", "Var"])

        st.markdown("**Ar-Ge ve fikri mülkiyet**")
        r_and_d_history = st.text_area("Mevcut Ar-Ge proje geçmişi", height=70)
        patent_brand_info = st.text_area("Patent / marka / faydalı model bilgileri", height=70)
        export_info = st.text_input("İhracat bilgisi")
        investment_incentive_history = st.text_input("Yatırım / teşvik geçmişi")

        uploaded = st.file_uploader(
            "Belgeler (PDF/Word/Excel/görsel) — MVP'de bilgi amaçlı saklanır",
            accept_multiple_files=True,
        )
        submitted = st.form_submit_button("Profili Kaydet", type="primary")

    if submitted:
        if not company_name.strip():
            st.error("Şirket unvanı zorunludur.")
            return
        profile = CompanyProfile(
            company_name=company_name.strip(),
            establishment_year=int(establishment_year),
            activity_area=activity_area or None,
            nace_code=nace_code or None,
            employee_count=int(employee_count) or None,
            sme_status=sme_status or None,
            balance_sheet_summary=balance_sheet_summary or None,
            net_sales=net_sales or None,
            total_assets=total_assets or None,
            tax_debt_status=tax_debt_status or None,
            sgk_debt_status=sgk_debt_status or None,
            r_and_d_history=r_and_d_history or None,
            patent_brand_info=patent_brand_info or None,
            export_info=export_info or None,
            investment_incentive_history=investment_incentive_history or None,
            uploaded_documents=[f.name for f in uploaded] if uploaded else [],
        )
        save_profile("company", profile)
        st.success("✅ Şirket profili kaydedildi.")
